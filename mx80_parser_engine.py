"""
Parser engine for Juniper MX80 CLI outputs
Uses pyATS/Genie primarily, regex as fallback
"""

import re
from typing import Optional, Dict, Any
from genie.conf.base import Device
from genie.libs.parser.junos.show_arp import ShowArpNoResolve as GenieShowArpNoResolve
from mx80_models import (
    ShowArpNoResolve, ShowArpNoResolveEntry,
    ShowVrrpSummary, ShowVrrpSummaryEntry, ShowVrrpSummaryAddress,
    ShowLldpNeighbors, ShowLldpNeighborsEntry,
    ShowBfdSession, ShowBfdSessionEntry,
    ShowRsvpNeighbor, ShowRsvpNeighborEntry
)


# ========================================
# show arp no-resolve | no-more
# ========================================

def parse_show_arp_no_resolve(cli_output: str) -> ShowArpNoResolve:
    """
    Parse 'show arp no-resolve | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowArpNoResolve object with parsed ARP entries
    """
    
    # Try pyATS/Genie first
    try:
        device = Device("mx80", os="junos")
        parser = GenieShowArpNoResolve(device=device)
        parsed_data = parser.parse(output=cli_output)
        
        arp_table = _convert_genie_show_arp_no_resolve(parsed_data)
        
        return arp_table
        
    except Exception as e:
        print(f"[WARN] Genie parsing failed: {type(e).__name__}: {e}")
        print(f"[INFO] Falling back to regex parsing...")
        
        return _parse_show_arp_no_resolve_regex(cli_output)


def _convert_genie_show_arp_no_resolve(genie_data: Dict[str, Any]) -> ShowArpNoResolve:
    """Convert Genie parser output to ShowArpNoResolve model"""
    arp_table = ShowArpNoResolve()
    
    if 'arp-table-information' in genie_data:
        arp_info = genie_data['arp-table-information']
        
        if 'arp-table-entry' in arp_info:
            for entry_data in arp_info['arp-table-entry']:
                entry = ShowArpNoResolveEntry(
                    mac_address=entry_data.get('mac-address', 'unknown'),
                    ip_address=entry_data.get('ip-address', 'unknown'),
                    interface=entry_data.get('interface-name', 'unknown'),
                    flags=entry_data.get('arp-table-entry-flags', 'none')
                )
                arp_table.entries.append(entry)
        
        if 'arp-entry-count' in arp_info:
            arp_table.total_entries = int(arp_info['arp-entry-count'])
        else:
            arp_table.total_entries = len(arp_table.entries)
    
    return arp_table


def _parse_show_arp_no_resolve_regex(cli_output: str) -> ShowArpNoResolve:
    """Regex-based fallback parser for ARP output"""
    arp_table = ShowArpNoResolve()
    
    total_match = re.search(r'Total entries:\s*(\d+)', cli_output)
    if total_match:
        arp_table.total_entries = int(total_match.group(1))
    
    pattern = r'^([0-9a-f:]+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\S+)\s+(\S+)'
    
    for line in cli_output.split('\n'):
        match = re.match(pattern, line.strip(), re.IGNORECASE)
        if match:
            entry = ShowArpNoResolveEntry(
                mac_address=match.group(1),
                ip_address=match.group(2),
                interface=match.group(3),
                flags=match.group(4)
            )
            arp_table.entries.append(entry)
    
    if arp_table.total_entries == 0:
        arp_table.total_entries = len(arp_table.entries)
    
    return arp_table


# ========================================
# show vrrp summary | no-more
# ========================================

def parse_show_vrrp_summary(cli_output: str) -> ShowVrrpSummary:
    """
    Parse 'show vrrp summary | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowVrrpSummary object with parsed VRRP entries
    """
    
    # No Genie parser available for VRRP on Junos - use regex directly
    return _parse_show_vrrp_summary_regex(cli_output)


def _convert_genie_show_vrrp_summary(genie_data: Dict[str, Any]) -> ShowVrrpSummary:
    """Convert Genie parser output to ShowVrrpSummary model"""
    # Not used - no Genie parser for VRRP
    vrrp_summary = ShowVrrpSummary()
    return vrrp_summary


def _parse_show_vrrp_summary_regex(cli_output: str) -> ShowVrrpSummary:
    """
    Regex-based fallback parser for VRRP summary output
    
    Format:
    Interface     State       Group   VR state       VR Mode    Type   Address 
    ge-1/1/5.605  up              1   master          Active    lcl    100.70.16.19       
                                                                vip    100.70.16.17
    """
    vrrp_summary = ShowVrrpSummary()
    
    lines = cli_output.split('\n')
    current_entry = None
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('Interface'):
            continue
        
        # Check if this is a main entry line (has interface)
        main_pattern = r'^(\S+)\s+(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
        main_match = re.match(main_pattern, line)
        
        if main_match:
            # Save previous entry if exists
            if current_entry:
                vrrp_summary.entries.append(current_entry)
            
            # Create new entry
            current_entry = ShowVrrpSummaryEntry(
                interface=main_match.group(1),
                state=main_match.group(2),
                group=int(main_match.group(3)),
                vr_state=main_match.group(4),
                vr_mode=main_match.group(5),
                addresses=[]
            )
            
            # Add first address
            addr = ShowVrrpSummaryAddress(
                type=main_match.group(6),
                address=main_match.group(7)
            )
            current_entry.addresses.append(addr)
        
        else:
            # Check if this is a continuation line (additional address)
            cont_pattern = r'^\s+(\S+)\s+(\S+)$'
            cont_match = re.match(cont_pattern, line)
            
            if cont_match and current_entry:
                addr = ShowVrrpSummaryAddress(
                    type=cont_match.group(1),
                    address=cont_match.group(2)
                )
                current_entry.addresses.append(addr)
    
    # Don't forget the last entry
    if current_entry:
        vrrp_summary.entries.append(current_entry)
    
    return vrrp_summary


# ========================================
# show lldp neighbors | no-more
# ========================================

def parse_show_lldp_neighbors(cli_output: str) -> ShowLldpNeighbors:
    """
    Parse 'show lldp neighbors | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowLldpNeighbors object with parsed LLDP entries
    """
    
    # No Genie parser available for LLDP on Junos - use regex directly
    return _parse_show_lldp_neighbors_regex(cli_output)


def _parse_show_lldp_neighbors_regex(cli_output: str) -> ShowLldpNeighbors:
    """
    Regex-based parser for LLDP neighbors output
    
    Format:
    Local Interface    Parent Interface    Chassis Id          Port info          System Name
    xe-0/0/2           -                   3c:8a:b0:8a:42:28   xe-0/0/2           ASXPER01.mynetwork.bolt.net
    """
    lldp_neighbors = ShowLldpNeighbors()
    
    lines = cli_output.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith('Local Interface'):
            continue
        
        # Pattern to match LLDP neighbor entry
        # Allows for any number of spaces between fields
        pattern = r'^(\S+)\s+(\S+)\s+([0-9a-f:]+)\s+(\S+)\s+(.+)$'
        match = re.match(pattern, line, re.IGNORECASE)
        
        if match:
            entry = ShowLldpNeighborsEntry(
                local_interface=match.group(1),
                parent_interface=match.group(2),
                chassis_id=match.group(3),
                port_info=match.group(4),
                system_name=match.group(5).strip()
            )
            lldp_neighbors.entries.append(entry)
    
    return lldp_neighbors


# ========================================
# show bfd session | no-more
# ========================================

def parse_show_bfd_session(cli_output: str) -> ShowBfdSession:
    """
    Parse 'show bfd session | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowBfdSession object with parsed BFD entries
    """
    
    # No Genie parser available for BFD on Junos - use regex directly
    return _parse_show_bfd_session_regex(cli_output)


def _parse_show_bfd_session_regex(cli_output: str) -> ShowBfdSession:
    """
    Regex-based parser for BFD session output
    
    Format:
                                                      Detect   Transmit
    Address                  State     Interface      Time     Interval  Multiplier
    194.180.106.154          Up        xe-0/0/3.0     0.300     0.100        3   
    
    2 sessions, 2 clients
    Cumulative transmit rate 20.0 pps, cumulative receive rate 20.0 pps
    """
    bfd_session = ShowBfdSession()
    
    lines = cli_output.split('\n')
    
    for line in lines:
        line_stripped = line.strip()
        
        # Skip empty lines and header lines
        if not line_stripped or 'Address' in line_stripped or 'Detect' in line_stripped:
            continue
        
        # Parse session entry
        pattern = r'^(\d+\.\d+\.\d+\.\d+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)'
        match = re.match(pattern, line_stripped)
        
        if match:
            entry = ShowBfdSessionEntry(
                address=match.group(1),
                state=match.group(2),
                interface=match.group(3),
                detect_time=match.group(4),
                transmit_interval=match.group(5),
                multiplier=match.group(6)
            )
            bfd_session.entries.append(entry)
        
        # Parse summary line: "2 sessions, 2 clients"
        summary_match = re.search(r'(\d+)\s+sessions?,\s+(\d+)\s+clients?', line_stripped)
        if summary_match:
            bfd_session.total_sessions = int(summary_match.group(1))
            bfd_session.total_clients = int(summary_match.group(2))
        
        # Parse cumulative rates
        rate_match = re.search(r'Cumulative transmit rate\s+(\S+\s+pps),\s+cumulative receive rate\s+(\S+\s+pps)', line_stripped)
        if rate_match:
            bfd_session.cumulative_transmit_rate = rate_match.group(1)
            bfd_session.cumulative_receive_rate = rate_match.group(2)
    
    return bfd_session


# ========================================
# show rsvp neighbor | no-more
# ========================================

def parse_show_rsvp_neighbor(cli_output: str) -> ShowRsvpNeighbor:
    """
    Parse 'show rsvp neighbor | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowRsvpNeighbor object with parsed RSVP neighbor entries
    """
    
    # No Genie parser available for RSVP neighbor on Junos - use regex directly
    return _parse_show_rsvp_neighbor_regex(cli_output)


def _parse_show_rsvp_neighbor_regex(cli_output: str) -> ShowRsvpNeighbor:
    """
    Regex-based parser for RSVP neighbor output
    
    Format:
    RSVP neighbor: 4 learned
    Address            Idle Up/Dn LastChange HelloInt HelloTx/Rx MsgRcvd
    194.180.107.35        0  1/0  69w1d 21:24:27        9 4654964/4654963 3869
    """
    rsvp_neighbor = ShowRsvpNeighbor()
    
    lines = cli_output.split('\n')
    
    for line in lines:
        line_stripped = line.strip()
        
        # Parse header line to get total neighbors
        header_match = re.search(r'RSVP neighbor:\s+(\d+)\s+learned', line_stripped)
        if header_match:
            rsvp_neighbor.total_neighbors = int(header_match.group(1))
            continue
        
        # Skip empty lines and header lines
        if not line_stripped or 'Address' in line_stripped or 'Idle' in line_stripped:
            continue
        
        # Parse neighbor entry - more flexible pattern to handle varying spaces in LastChange
        pattern = r'^(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s+(\d+/\d+)\s+(.+?)\s+(\d+)\s+(\d+/\d+)\s+(\d+)$'
        match = re.match(pattern, line_stripped)
        
        if match:
            entry = ShowRsvpNeighborEntry(
                address=match.group(1),
                idle=match.group(2),
                up_dn=match.group(3),
                last_change=match.group(4).strip(),
                hello_interval=match.group(5),
                hello_tx_rx=match.group(6),
                msg_rcvd=match.group(7)
            )
            rsvp_neighbor.entries.append(entry)
    
    # If total_neighbors wasn't set from header, use entry count
    if rsvp_neighbor.total_neighbors == 0:
        rsvp_neighbor.total_neighbors = len(rsvp_neighbor.entries)
    
    return rsvp_neighbor


# ========================================
# Main execution
# ========================================

if __name__ == "__main__":
    import json
    from command_segmenter import (
        read_mx80_show_commands, 
        extract_show_arp_output_1,
        extract_show_vrrp_summary_output_2,
        extract_show_lldp_neighbors_output_3,
        extract_show_bfd_session_output_4,
        extract_show_rsvp_neighbor_output_5
    )
    
    raw_output = read_mx80_show_commands("juniper_show_command.txt")
    
    # Test show arp no-resolve
    print("=" * 50)
    print("show arp no-resolve | no-more")
    print("=" * 50)
    arp_output = extract_show_arp_output_1(raw_output)
    arp_result = parse_show_arp_no_resolve(arp_output)
    print(json.dumps(arp_result.to_dict(), indent=2))
    
    # Test show vrrp summary
    print("\n" + "=" * 50)
    print("show vrrp summary | no-more")
    print("=" * 50)
    vrrp_output = extract_show_vrrp_summary_output_2(raw_output)
    vrrp_result = parse_show_vrrp_summary(vrrp_output)
    print(json.dumps(vrrp_result.to_dict(), indent=2))
    
    # Test show lldp neighbors
    print("\n" + "=" * 50)
    print("show lldp neighbors | no-more")
    print("=" * 50)
    lldp_output = extract_show_lldp_neighbors_output_3(raw_output)
    lldp_result = parse_show_lldp_neighbors(lldp_output)
    print(json.dumps(lldp_result.to_dict(), indent=2))
    
    # Test show bfd session
    print("\n" + "=" * 50)
    print("show bfd session | no-more")
    print("=" * 50)
    bfd_output = extract_show_bfd_session_output_4(raw_output)
    bfd_result = parse_show_bfd_session(bfd_output)
    print(json.dumps(bfd_result.to_dict(), indent=2))
    
    # Test show rsvp neighbor
    print("\n" + "=" * 50)
    print("show rsvp neighbor | no-more")
    print("=" * 50)
    rsvp_output = extract_show_rsvp_neighbor_output_5(raw_output)
    rsvp_result = parse_show_rsvp_neighbor(rsvp_output)
    print(json.dumps(rsvp_result.to_dict(), indent=2))