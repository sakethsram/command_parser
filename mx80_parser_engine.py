"""
Parser engine for Juniper MX80 CLI outputs
Uses pyATS/Genie primarily, regex as fallback
"""

import re
import json
from typing import Optional, Dict, Any
from genie.conf.base import Device
from genie.libs.parser.junos.show_arp import ShowArpNoResolve as GenieShowArpNoResolve

from mx80_models import (
    ShowArpNoResolve, ShowArpNoResolveEntry,
    ShowVrrpSummary, ShowVrrpSummaryEntry, ShowVrrpSummaryAddress,
    ShowLldpNeighbors, ShowLldpNeighborsEntry,
    ShowBfdSession, ShowBfdSessionEntry,
    ShowRsvpNeighbor, ShowRsvpNeighborEntry,
    ShowRsvpSession, ShowRsvpSessionSection, ShowRsvpSessionEntry,
    ShowRouteTableInet0, ShowRouteTableInet0Entry,
    ShowRouteTableInet3, ShowRouteTableInet3Entry, ShowRouteTableInet3NextHop,
    ShowRouteTableMpls0, ShowRouteTableMpls0Entry, ShowRouteTableMpls0NextHop,
    ShowMplsInterface, ShowMplsInterfaceEntry,
    ShowMplsLsp, ShowMplsLspSection, ShowMplsLspEntry,
    ShowMplsLspP2mp, ShowMplsLspP2mpSection, ShowMplsLspP2mpGroup, ShowMplsLspP2mpEntry,
    ShowBgpSummary, ShowBgpSummaryTable, ShowBgpSummaryPeer, ShowBgpSummaryPeerRib,
    ShowBgpNeighbor, ShowBgpNeighborEntry, ShowBgpNeighborTable,
    ShowIsisAdjacencyExtensive, ShowIsisAdjacencyEntry, ShowIsisAdjacencyTransition,
    ShowRouteSummary, ShowRouteSummaryTable, ShowRouteSummaryProtocol, ShowRouteSummaryHighwater
)

from command_segmenter import (
    read_mx80_show_commands,
    extract_show_arp_output_1,
    extract_show_vrrp_summary_output_2,
    extract_show_lldp_neighbors_output_3,
    extract_show_bfd_session_output_4,
    extract_show_rsvp_neighbor_output_5,
    extract_show_rsvp_session_output_6,
    extract_show_route_table_inet0_output_7,
    extract_show_route_table_inet3_output_8,
    extract_show_route_table_mpls0_output_9,
    extract_show_mpls_interface_output_10,
    extract_show_mpls_lsp_output_11,
    extract_show_mpls_lsp_p2mp_output_12,
    extract_show_bgp_summary_output_13,
    extract_show_bgp_neighbor_output_14,
    extract_show_isis_adjacency_extensive_output_15,
    extract_show_route_summary_output_16,
    extract_show_rsvp_session_match_dn_output_17,
    extract_show_mpls_lsp_unidirectional_match_dn_output_18,
    extract_show_rsvp_session_first_output_19,
    extract_show_rsvp_session_second_output_20,
    extract_show_rsvp_session_ma_output_21,
    extract_show_mpls_lsp_unidirectional_output_22,
)
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
def parse_show_rsvp_session(cli_output: str) -> ShowRsvpSession:
    """
    Parse 'show rsvp session | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowRsvpSession object with parsed RSVP session entries
    """
    
    # No Genie parser available for RSVP session on Junos - use regex directly
    return _parse_show_rsvp_session_regex(cli_output)


def _parse_show_rsvp_session_regex(cli_output: str) -> ShowRsvpSession:
    """
    Regex-based parser for RSVP session output
    
    Format has three sections: Ingress, Egress, Transit
    Each section has entries with: To, From, State, Rt, Style, Labelin, Labelout, LSPname
    """
    rsvp_session = ShowRsvpSession()
    
    lines = cli_output.split('\n')
    current_section = None
    current_section_type = None
    
    for line in lines:
        line_stripped = line.strip()
        
        # Skip empty lines
        if not line_stripped:
            continue
        
        # Parse section headers: "Ingress RSVP: 21 sessions"
        ingress_match = re.search(r'Ingress RSVP:\s+(\d+)\s+sessions?', line_stripped)
        if ingress_match:
            current_section = ShowRsvpSessionSection(
                section_type='Ingress',
                total_sessions=int(ingress_match.group(1))
            )
            rsvp_session.ingress = current_section
            current_section_type = 'Ingress'
            continue
        
        egress_match = re.search(r'Egress RSVP:\s+(\d+)\s+sessions?', line_stripped)
        if egress_match:
            current_section = ShowRsvpSessionSection(
                section_type='Egress',
                total_sessions=int(egress_match.group(1))
            )
            rsvp_session.egress = current_section
            current_section_type = 'Egress'
            continue
        
        transit_match = re.search(r'Transit RSVP:\s+(\d+)\s+sessions?', line_stripped)
        if transit_match:
            current_section = ShowRsvpSessionSection(
                section_type='Transit',
                total_sessions=int(transit_match.group(1))
            )
            rsvp_session.transit = current_section
            current_section_type = 'Transit'
            continue
        
        # Skip header lines
        if 'To' in line_stripped and 'From' in line_stripped and 'State' in line_stripped:
            continue
        
        # Parse summary line: "Total 21 displayed, Up 21, Down 0"
        summary_match = re.search(r'Total\s+(\d+)\s+displayed,\s+Up\s+(\d+),\s+Down\s+(\d+)', line_stripped)
        if summary_match and current_section:
            current_section.total_displayed = int(summary_match.group(1))
            current_section.total_up = int(summary_match.group(2))
            current_section.total_down = int(summary_match.group(3))
            continue
        
        # Parse session entry
        # Pattern: To From State Rt Style Labelin Labelout LSPname
        # Need to handle IP addresses and '-' for missing values
        pattern = r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+.*)$'
        match = re.match(pattern, line_stripped)
        
        if match and current_section:
            entry = ShowRsvpSessionEntry(
                to=match.group(1),
                from_addr=match.group(2),
                state=match.group(3),
                rt=match.group(4),
                style=match.group(5) + ' ' + match.group(6),  # "1 SE"
                labelin=match.group(7),
                labelout=match.group(8),
                lspname=match.group(9).strip() if len(match.groups()) >= 9 else ""
            )
            current_section.entries.append(entry)
    
    return rsvp_session
# ========================================
# show route table inet.0 | no-more
# ========================================

def parse_show_route_table_inet0(cli_output: str) -> ShowRouteTableInet0:
    """
    Parse 'show route table inet.0 | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowRouteTableInet0 object with parsed routing entries
    """
    
    return _parse_show_route_table_inet0_regex(cli_output)


def _parse_show_route_table_inet0_regex(cli_output: str) -> ShowRouteTableInet0:
    """
    Regex-based parser for inet.0 routing table output
    
    Format:
    inet.0: 197 destinations, 197 routes (195 active, 0 holddown, 2 hidden)
    10.5.0.0/16        *[IS-IS/18] 2d 05:55:40, metric 128960
                        >  to 194.180.106.154 via xe-0/0/3.0
    """
    route_table = ShowRouteTableInet0()
    
    lines = cli_output.split('\n')
    current_entry = None
    
    for line in lines:
        line_stripped = line.strip()
        
        # Parse header: "inet.0: 197 destinations, 197 routes (195 active, 0 holddown, 2 hidden)"
        header_match = re.search(r'inet\.0:\s+(\d+)\s+destinations,\s+(\d+)\s+routes\s+\((\d+)\s+active,\s+(\d+)\s+holddown,\s+(\d+)\s+hidden\)', line_stripped)
        if header_match:
            route_table.total_destinations = int(header_match.group(1))
            route_table.total_routes = int(header_match.group(2))
            route_table.active_routes = int(header_match.group(3))
            route_table.holddown_routes = int(header_match.group(4))
            route_table.hidden_routes = int(header_match.group(5))
            continue
        
        # Skip legend and empty lines
        if not line_stripped or line_stripped.startswith('+') or line_stripped.startswith('-'):
            continue
        
        # Parse main route entry: "10.5.0.0/16        *[IS-IS/18] 2d 05:55:40, metric 128960"
        main_pattern = r'^(\S+)\s+\*\[([^\]]+)\]\s+([^,]+),\s+metric\s+(\S+)'
        main_match = re.match(main_pattern, line_stripped)
        
        if main_match:
            # Save previous entry
            if current_entry:
                route_table.entries.append(current_entry)
            
            # Parse protocol and preference
            protocol_pref = main_match.group(2).split('/')
            protocol = protocol_pref[0] if len(protocol_pref) > 0 else ""
            preference = protocol_pref[1] if len(protocol_pref) > 1 else ""
            
            current_entry = ShowRouteTableInet0Entry(
                destination=main_match.group(1),
                protocol=protocol,
                preference=preference,
                age=main_match.group(3).strip(),
                metric=main_match.group(4),
                next_hop="",
                via=""
            )
        
        # Parse next-hop line: ">  to 194.180.106.154 via xe-0/0/3.0"
        elif current_entry:
            nexthop_pattern = r'>\s+to\s+(\S+)\s+via\s+(\S+)(?:,\s+(.+))?'
            nexthop_match = re.search(nexthop_pattern, line_stripped)
            
            if nexthop_match:
                current_entry.next_hop = nexthop_match.group(1)
                current_entry.via = nexthop_match.group(2)
                if nexthop_match.group(3):
                    current_entry.mpls_label = nexthop_match.group(3)
            
            # Handle Direct/Local routes
            elif 'Direct' in line or 'Local' in line:
                local_pattern = r'(\S+)\s+via\s+(\S+)'
                local_match = re.search(local_pattern, line_stripped)
                if local_match:
                    current_entry.next_hop = local_match.group(1)
                    current_entry.via = local_match.group(2)
    
    # Don't forget last entry
    if current_entry:
        route_table.entries.append(current_entry)
    
    return route_table


# ========================================
# show route table inet.3 | no-more
# ========================================

def parse_show_route_table_inet3(cli_output: str) -> ShowRouteTableInet3:
    """
    Parse 'show route table inet.3 | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowRouteTableInet3 object with parsed routing entries
    """
    
    return _parse_show_route_table_inet3_regex(cli_output)


def _parse_show_route_table_inet3_regex(cli_output: str) -> ShowRouteTableInet3:
    """
    Regex-based parser for inet.3 routing table output
    
    Format with multiple next-hops:
    10.210.0.5/32      *[L-ISIS/6] 1w3d 23:36:09, metric 57750
                        >  to 194.180.106.156 via xe-0/0/2.0, Push 163028
                           to 194.180.106.154 via xe-0/0/3.0, Push 163028
    """
    route_table = ShowRouteTableInet3()
    
    lines = cli_output.split('\n')
    current_entry = None
    
    for line in lines:
        line_stripped = line.strip()
        
        # Parse header
        header_match = re.search(r'inet\.3:\s+(\d+)\s+destinations,\s+(\d+)\s+routes\s+\((\d+)\s+active,\s+(\d+)\s+holddown,\s+(\d+)\s+hidden\)', line_stripped)
        if header_match:
            route_table.total_destinations = int(header_match.group(1))
            route_table.total_routes = int(header_match.group(2))
            route_table.active_routes = int(header_match.group(3))
            route_table.holddown_routes = int(header_match.group(4))
            route_table.hidden_routes = int(header_match.group(5))
            continue
        
        # Skip legend and empty lines
        if not line_stripped or line_stripped.startswith('+') or line_stripped.startswith('-'):
            continue
        
        # Parse main route entry
        main_pattern = r'^(\S+)\s+\*\[([^\]]+)\]\s+([^,]+),\s+metric\s+(\S+)'
        main_match = re.match(main_pattern, line_stripped)
        
        if main_match:
            # Save previous entry
            if current_entry:
                route_table.entries.append(current_entry)
            
            # Parse protocol and preference
            protocol_pref = main_match.group(2).split('/')
            protocol = protocol_pref[0] if len(protocol_pref) > 0 else ""
            preference = protocol_pref[1] if len(protocol_pref) > 1 else ""
            
            current_entry = ShowRouteTableInet3Entry(
                destination=main_match.group(1),
                protocol=protocol,
                preference=preference,
                age=main_match.group(3).strip(),
                metric=main_match.group(4),
                next_hops=[]
            )
        
        # Parse next-hop lines
        elif current_entry:
            # Pattern for next-hop with or without '>'
            nexthop_pattern = r'(?:>\s+)?to\s+(\S+)\s+via\s+(\S+)(?:,\s+(.+))?'
            nexthop_match = re.search(nexthop_pattern, line_stripped)
            
            if nexthop_match:
                nh = ShowRouteTableInet3NextHop(
                    to=nexthop_match.group(1),
                    via=nexthop_match.group(2),
                    mpls_label=nexthop_match.group(3) if nexthop_match.group(3) else ""
                )
                current_entry.next_hops.append(nh)
            
            # Handle special cases like "Discard"
            elif 'Discard' in line_stripped:
                nh = ShowRouteTableInet3NextHop(
                    to="",
                    via="Discard",
                    mpls_label=""
                )
                current_entry.next_hops.append(nh)
    
    # Don't forget last entry
    if current_entry:
        route_table.entries.append(current_entry)
    
    return route_table


# ========================================
# show route table mpls.0 | no-more
# ========================================

def parse_show_route_table_mpls0(cli_output: str) -> ShowRouteTableMpls0:
    """
    Parse 'show route table mpls.0 | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowRouteTableMpls0 object with parsed MPLS routing entries
    """
    
    return _parse_show_route_table_mpls0_regex(cli_output)


def _parse_show_route_table_mpls0_regex(cli_output: str) -> ShowRouteTableMpls0:
    """
    Regex-based parser for mpls.0 routing table output
    
    Format:
    0                  *[MPLS/0] 69w1d 21:26:41, metric 1
                           to table inet.0
    5820               *[RSVP/7/1] 1w3d 23:35:53, metric 1
                        >  to 194.180.106.154 via xe-0/0/3.0, label-switched-path Bypass->194.180.106.152
    """
    route_table = ShowRouteTableMpls0()
    
    lines = cli_output.split('\n')
    current_entry = None
    
    for line in lines:
        line_stripped = line.strip()
        
        # Parse header
        header_match = re.search(r'mpls\.0:\s+(\d+)\s+destinations,\s+(\d+)\s+routes\s+\((\d+)\s+active,\s+(\d+)\s+holddown,\s+(\d+)\s+hidden\)', line_stripped)
        if header_match:
            route_table.total_destinations = int(header_match.group(1))
            route_table.total_routes = int(header_match.group(2))
            route_table.active_routes = int(header_match.group(3))
            route_table.holddown_routes = int(header_match.group(4))
            route_table.hidden_routes = int(header_match.group(5))
            continue
        
        # Skip legend and empty lines
        if not line_stripped or line_stripped.startswith('+') or line_stripped.startswith('-'):
            continue
        
        # Parse main MPLS label entry
        main_pattern = r'^(\S+)\s+\*\[([^\]]+)\]\s+([^,]+),\s+metric\s+(\S+)'
        main_match = re.match(main_pattern, line_stripped)
        
        if main_match:
            # Save previous entry
            if current_entry:
                route_table.entries.append(current_entry)
            
            # Parse protocol and preference
            protocol_parts = main_match.group(2).split('/')
            protocol = protocol_parts[0] if len(protocol_parts) > 0 else ""
            preference = '/'.join(protocol_parts[1:]) if len(protocol_parts) > 1 else ""
            
            current_entry = ShowRouteTableMpls0Entry(
                label=main_match.group(1),
                protocol=protocol,
                preference=preference,
                age=main_match.group(3).strip(),
                metric=main_match.group(4),
                next_hops=[]
            )
        
        # Parse next-hop lines
        elif current_entry:
            # Pattern: "to table inet.0"
            if 'to table' in line_stripped:
                table_match = re.search(r'to table\s+(\S+)', line_stripped)
                if table_match:
                    nh = ShowRouteTableMpls0NextHop(
                        to="table",
                        via=table_match.group(1),
                        action=""
                    )
                    current_entry.next_hops.append(nh)
            
            # Pattern: "Receive", "Discard"
            elif re.match(r'^\s*(Receive|Discard)\s*$', line_stripped):
                nh = ShowRouteTableMpls0NextHop(
                    action=line_stripped
                )
                current_entry.next_hops.append(nh)
            
            # Pattern: "via lsi.0 (CUST-AUTUMN_COMPASS-ADMIN-CXA02), Pop"
            elif 'via lsi' in line_stripped or 'via vt-' in line_stripped or 'via ms-' in line_stripped:
                via_pattern = r'via\s+(\S+)(?:\s+\(([^)]+)\))?,\s+(\S+)'
                via_match = re.search(via_pattern, line_stripped)
                if via_match:
                    nh = ShowRouteTableMpls0NextHop(
                        via=via_match.group(1),
                        lsp_name=via_match.group(2) if via_match.group(2) else "",
                        action=via_match.group(3)
                    )
                    current_entry.next_hops.append(nh)
            
            # Pattern: ">  to 194.180.106.154 via xe-0/0/3.0, label-switched-path Bypass->194.180.106.152"
            elif 'to' in line_stripped and 'via' in line_stripped:
                lsp_pattern = r'(?:>\s+)?to\s+(\S+)\s+via\s+(\S+)(?:,\s+label-switched-path\s+(.+))?(?:,\s+(Swap|Pop|Push)\s+(.+))?'
                lsp_match = re.search(lsp_pattern, line_stripped)
                if lsp_match:
                    nh = ShowRouteTableMpls0NextHop(
                        to=lsp_match.group(1),
                        via=lsp_match.group(2),
                        lsp_name=lsp_match.group(3) if lsp_match.group(3) else "",
                        mpls_label=""
                    )
                    current_entry.next_hops.append(nh)
                else:
                    # Simpler pattern for Swap/Pop operations
                    simple_pattern = r'(?:>\s+)?to\s+(\S+)\s+via\s+(\S+)(?:,\s+(.+))?'
                    simple_match = re.search(simple_pattern, line_stripped)
                    if simple_match:
                        nh = ShowRouteTableMpls0NextHop(
                            to=simple_match.group(1),
                            via=simple_match.group(2),
                            mpls_label=simple_match.group(3) if simple_match.group(3) else ""
                        )
                        current_entry.next_hops.append(nh)
    
    # Don't forget last entry
    if current_entry:
        route_table.entries.append(current_entry)
    
    return route_table
# ========================================
# show mpls interface | no-more
# ========================================

def parse_show_mpls_interface(cli_output: str) -> ShowMplsInterface:
    """
    Parse 'show mpls interface | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowMplsInterface object with parsed MPLS interface entries
    """
    
    return _parse_show_mpls_interface_regex(cli_output)


def _parse_show_mpls_interface_regex(cli_output: str) -> ShowMplsInterface:
    """
    Regex-based parser for MPLS interface output
    
    Format:
    Interface        State       Administrative groups (x: extended)
    xe-0/0/2.0       Up          SHUNT
    """
    mpls_interface = ShowMplsInterface()
    
    lines = cli_output.split('\n')
    
    for line in lines:
        line_stripped = line.strip()
        
        # Skip header and empty lines
        if not line_stripped or 'Interface' in line_stripped:
            continue
        
        # Parse interface entry
        pattern = r'^(\S+)\s+(\S+)\s+(.+)$'
        match = re.match(pattern, line_stripped)
        
        if match:
            entry = ShowMplsInterfaceEntry(
                interface=match.group(1),
                state=match.group(2),
                administrative_groups=match.group(3).strip()
            )
            mpls_interface.entries.append(entry)
    
    return mpls_interface


# ========================================
# show mpls lsp | no-more
# ========================================

def parse_show_mpls_lsp(cli_output: str) -> ShowMplsLsp:
    """
    Parse 'show mpls lsp | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowMplsLsp object with parsed MPLS LSP entries
    """
    
    return _parse_show_mpls_lsp_regex(cli_output)


def _parse_show_mpls_lsp_regex(cli_output: str) -> ShowMplsLsp:
    """
    Regex-based parser for MPLS LSP output
    
    Has three sections: Ingress, Egress, Transit
    Ingress has different format than Egress/Transit
    """
    mpls_lsp = ShowMplsLsp()
    
    lines = cli_output.split('\n')
    current_section = None
    current_section_type = None
    
    for line in lines:
        line_stripped = line.strip()
        
        # Skip empty lines
        if not line_stripped:
            continue
        
        # Parse section headers
        ingress_match = re.search(r'Ingress LSP:\s+(\d+)\s+sessions?', line_stripped)
        if ingress_match:
            current_section = ShowMplsLspSection(
                section_type='Ingress',
                total_sessions=int(ingress_match.group(1))
            )
            mpls_lsp.ingress = current_section
            current_section_type = 'Ingress'
            continue
        
        egress_match = re.search(r'Egress LSP:\s+(\d+)\s+sessions?', line_stripped)
        if egress_match:
            current_section = ShowMplsLspSection(
                section_type='Egress',
                total_sessions=int(egress_match.group(1))
            )
            mpls_lsp.egress = current_section
            current_section_type = 'Egress'
            continue
        
        transit_match = re.search(r'Transit LSP:\s+(\d+)\s+sessions?', line_stripped)
        if transit_match:
            current_section = ShowMplsLspSection(
                section_type='Transit',
                total_sessions=int(transit_match.group(1))
            )
            mpls_lsp.transit = current_section
            current_section_type = 'Transit'
            continue
        
        # Skip header lines
        if 'To' in line_stripped and 'From' in line_stripped:
            continue
        
        # Parse summary line
        summary_match = re.search(r'Total\s+(\d+)\s+displayed,\s+Up\s+(\d+),\s+Down\s+(\d+)', line_stripped)
        if summary_match and current_section:
            current_section.total_displayed = int(summary_match.group(1))
            current_section.total_up = int(summary_match.group(2))
            current_section.total_down = int(summary_match.group(3))
            continue
        
        # Parse LSP entry based on section type
        if current_section:
            if current_section_type == 'Ingress':
                # Ingress format: To From State Rt P ActivePath LSPname
                pattern = r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S*)\s+(.+)$'
                match = re.match(pattern, line_stripped)
                
                if match:
                    entry = ShowMplsLspEntry(
                        to=match.group(1),
                        from_addr=match.group(2),
                        state=match.group(3),
                        rt=match.group(4),
                        p=match.group(5),
                        active_path=match.group(6),
                        lspname=match.group(7).strip()
                    )
                    current_section.entries.append(entry)
            
            else:  # Egress or Transit
                # Format: To From State Rt Style Labelin Labelout LSPname
                pattern = r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.+)$'
                match = re.match(pattern, line_stripped)
                
                if match:
                    entry = ShowMplsLspEntry(
                        to=match.group(1),
                        from_addr=match.group(2),
                        state=match.group(3),
                        rt=match.group(4),
                        p="",
                        active_path="",
                        style=match.group(5) + ' ' + match.group(6),
                        labelin=match.group(7),
                        labelout=match.group(8),
                        lspname=match.group(9).strip()
                    )
                    current_section.entries.append(entry)
    
    return mpls_lsp


# ========================================
# show mpls lsp p2mp | no-more
# ========================================

def parse_show_mpls_lsp_p2mp(cli_output: str) -> ShowMplsLspP2mp:
    """
    Parse 'show mpls lsp p2mp | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowMplsLspP2mp object with parsed P2MP MPLS LSP entries
    """
    
    return _parse_show_mpls_lsp_p2mp_regex(cli_output)


def _parse_show_mpls_lsp_p2mp_regex(cli_output: str) -> ShowMplsLspP2mp:
    """
    Regex-based parser for MPLS LSP P2MP output
    
    Has P2MP groups with branch counts
    """
    mpls_lsp_p2mp = ShowMplsLspP2mp()
    
    lines = cli_output.split('\n')
    current_section = None
    current_section_type = None
    current_group = None
    
    for line in lines:
        line_stripped = line.strip()
        
        # Skip empty lines
        if not line_stripped:
            continue
        
        # Parse section headers
        ingress_match = re.search(r'Ingress LSP:\s+(\d+)\s+sessions?', line_stripped)
        if ingress_match:
            current_section = ShowMplsLspP2mpSection(
                section_type='Ingress',
                total_sessions=int(ingress_match.group(1))
            )
            mpls_lsp_p2mp.ingress = current_section
            current_section_type = 'Ingress'
            current_group = None
            continue
        
        egress_match = re.search(r'Egress LSP:\s+(\d+)\s+sessions?', line_stripped)
        if egress_match:
            current_section = ShowMplsLspP2mpSection(
                section_type='Egress',
                total_sessions=int(egress_match.group(1))
            )
            mpls_lsp_p2mp.egress = current_section
            current_section_type = 'Egress'
            current_group = None
            continue
        
        transit_match = re.search(r'Transit LSP:\s+(\d+)\s+sessions?', line_stripped)
        if transit_match:
            current_section = ShowMplsLspP2mpSection(
                section_type='Transit',
                total_sessions=int(transit_match.group(1))
            )
            mpls_lsp_p2mp.transit = current_section
            current_section_type = 'Transit'
            current_group = None
            continue
        
        # Parse P2MP name line
        p2mp_match = re.search(r'P2MP name:\s+(.+?),\s+P2MP branch count:\s+(\d+)', line_stripped)
        if p2mp_match and current_section:
            # Save previous group if exists
            if current_group:
                current_section.groups.append(current_group)
            
            # Create new group
            current_group = ShowMplsLspP2mpGroup(
                p2mp_name=p2mp_match.group(1).strip(),
                branch_count=int(p2mp_match.group(2))
            )
            continue
        
        # Skip header lines
        if 'To' in line_stripped and 'From' in line_stripped:
            continue
        
        # Parse summary line
        summary_match = re.search(r'Total\s+(\d+)\s+displayed,\s+Up\s+(\d+),\s+Down\s+(\d+)', line_stripped)
        if summary_match and current_section:
            # Save last group before summary
            if current_group:
                current_section.groups.append(current_group)
                current_group = None
            
            current_section.total_displayed = int(summary_match.group(1))
            current_section.total_up = int(summary_match.group(2))
            current_section.total_down = int(summary_match.group(3))
            continue
        
        # Parse LSP entry
        if current_group:
            if current_section_type == 'Ingress':
                # Ingress format: To From State Rt P ActivePath LSPname
                pattern = r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S*)\s+(.+)$'
                match = re.match(pattern, line_stripped)
                
                if match:
                    entry = ShowMplsLspP2mpEntry(
                        to=match.group(1),
                        from_addr=match.group(2),
                        state=match.group(3),
                        rt=match.group(4),
                        p=match.group(5),
                        active_path=match.group(6),
                        lspname=match.group(7).strip()
                    )
                    current_group.entries.append(entry)
            
            else:  # Egress or Transit
                # Format: To From State Rt Style Labelin Labelout LSPname
                pattern = r'^(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)\s+(.+)$'
                match = re.match(pattern, line_stripped)
                
                if match:
                    entry = ShowMplsLspP2mpEntry(
                        to=match.group(1),
                        from_addr=match.group(2),
                        state=match.group(3),
                        rt=match.group(4),
                        style=match.group(5) + ' ' + match.group(6),
                        labelin=match.group(7),
                        labelout=match.group(8),
                        lspname=match.group(9).strip()
                    )
                    current_group.entries.append(entry)
    
    # Don't forget last group
    if current_group and current_section:
        current_section.groups.append(current_group)
    
    return mpls_lsp_p2mp
# ========================================
# show bgp summary | no-more
# ========================================

def parse_show_bgp_summary(cli_output: str) -> ShowBgpSummary:
    """
    Parse 'show bgp summary | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowBgpSummary object with parsed BGP summary
    """
    
    return _parse_show_bgp_summary_regex(cli_output)


def _parse_show_bgp_summary_regex(cli_output: str) -> ShowBgpSummary:
    """Regex-based parser for BGP summary output"""
    bgp_summary = ShowBgpSummary()
    
    lines = cli_output.split('\n')
    current_peer = None
    in_table_section = False
    
    for line in lines:
        line_stripped = line.strip()
        
        # Parse threading mode
        if line_stripped.startswith('Threading mode:'):
            bgp_summary.threading_mode = line_stripped.split(':', 1)[1].strip()
            continue
        
        # Parse eBGP mode
        if line_stripped.startswith('Default eBGP mode:'):
            bgp_summary.default_ebgp_mode = line_stripped.split(':', 1)[1].strip()
            continue
        
        # Parse groups/peers
        groups_match = re.search(r'Groups:\s+(\d+)\s+Peers:\s+(\d+)\s+Down peers:\s+(\d+)', line_stripped)
        if groups_match:
            bgp_summary.groups = int(groups_match.group(1))
            bgp_summary.peers = int(groups_match.group(2))
            bgp_summary.down_peers = int(groups_match.group(3))
            continue
        
        # Parse table header
        if 'Table' in line_stripped and 'Tot Paths' in line_stripped:
            in_table_section = True
            continue
        
        # Parse table entries
        if in_table_section and not line_stripped.startswith('Peer'):
            if re.match(r'^[a-zA-Z]', line_stripped):
                # Table name line
                table_name = line_stripped
                continue
            elif re.match(r'^\d', line_stripped):
                # Table statistics line
                parts = line_stripped.split()
                if len(parts) >= 6:
                    table = ShowBgpSummaryTable(
                        table_name=table_name if 'table_name' in locals() else "",
                        total_paths=int(parts[0]),
                        active_paths=int(parts[1]),
                        suppressed=int(parts[2]),
                        history=int(parts[3]),
                        damp_state=int(parts[4]),
                        pending=int(parts[5])
                    )
                    bgp_summary.tables.append(table)
                continue
        
        # Parse peer header
        if line_stripped.startswith('Peer') and 'AS' in line_stripped:
            in_table_section = False
            continue
        
        # Parse peer entries
        peer_pattern = r'^(\S+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(.+?)\s+(Active|Establ|[A-Z]\S+)'
        peer_match = re.match(peer_pattern, line_stripped)
        
        if peer_match:
            if current_peer:
                bgp_summary.peer_list.append(current_peer)
            
            current_peer = ShowBgpSummaryPeer(
                peer=peer_match.group(1),
                asn=peer_match.group(2),
                in_pkt=peer_match.group(3),
                out_pkt=peer_match.group(4),
                out_q=peer_match.group(5),
                flaps=peer_match.group(6),
                last_up_dwn=peer_match.group(7).strip(),
                state=peer_match.group(8)
            )
        elif current_peer and line_stripped and ':' in line_stripped:
            # Parse RIB lines
            rib_parts = line_stripped.split(':')
            if len(rib_parts) == 2:
                rib = ShowBgpSummaryPeerRib(
                    table_name=rib_parts[0].strip(),
                    active_received_accepted_damped=rib_parts[1].strip()
                )
                current_peer.ribs.append(rib)
    
    # Don't forget last peer
    if current_peer:
        bgp_summary.peer_list.append(current_peer)
    
    return bgp_summary


# ========================================
# show bgp neighbor | no-more
# ========================================

def parse_show_bgp_neighbor(cli_output: str) -> ShowBgpNeighbor:
    """
    Parse 'show bgp neighbor | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowBgpNeighbor object with parsed BGP neighbor information
    """
    
    return _parse_show_bgp_neighbor_regex(cli_output)


def _parse_show_bgp_neighbor_regex(cli_output: str) -> ShowBgpNeighbor:
    """Regex-based parser for BGP neighbor output"""
    bgp_neighbor = ShowBgpNeighbor()
    
    lines = cli_output.split('\n')
    current_neighbor = None
    current_table = None
    
    for line in lines:
        line_stripped = line.strip()
        
        # Parse peer header
        peer_match = re.match(r'^Peer:\s+(\S+)\s+AS\s+(\d+)\s+Local:\s+(\S+)\s+AS\s+(\d+)', line_stripped)
        if peer_match:
            if current_neighbor:
                bgp_neighbor.neighbors.append(current_neighbor)
            
            current_neighbor = ShowBgpNeighborEntry(
                peer=peer_match.group(1),
                peer_as=peer_match.group(2),
                local=peer_match.group(3),
                local_as=peer_match.group(4)
            )
            current_table = None
            continue
        
        if not current_neighbor:
            continue
        
        # Parse description
        if line_stripped.startswith('Description:'):
            current_neighbor.description = line_stripped.split(':', 1)[1].strip()
        
        # Parse group
        elif line_stripped.startswith('Group:'):
            parts = line_stripped.split()
            if len(parts) >= 2:
                current_neighbor.group = parts[1]
            if 'Routing-Instance:' in line_stripped:
                current_neighbor.routing_instance = line_stripped.split('Routing-Instance:')[1].strip()
        
        # Parse type/state
        elif line_stripped.startswith('Type:'):
            type_match = re.search(r'Type:\s+(\S+)\s+State:\s+(\S+)', line_stripped)
            if type_match:
                current_neighbor.type = type_match.group(1)
                current_neighbor.state = type_match.group(2)
        
        # Parse local address
        elif 'Local Address:' in line_stripped:
            addr_match = re.search(r'Local Address:\s+(\S+)\s+Holdtime:\s+(\d+)', line_stripped)
            if addr_match:
                current_neighbor.local_address = addr_match.group(1)
                current_neighbor.holdtime = addr_match.group(2)
        
        # Parse flaps
        elif line_stripped.startswith('Number of flaps:'):
            flaps_match = re.search(r'Number of flaps:\s+(\d+)', line_stripped)
            if flaps_match:
                current_neighbor.number_of_flaps = int(flaps_match.group(1))
        
        # Parse table
        elif line_stripped.startswith('Table '):
            table_match = re.match(r'Table\s+(\S+)', line_stripped)
            if table_match:
                current_table = ShowBgpNeighborTable(
                    table_name=table_match.group(1)
                )
                current_neighbor.tables.append(current_table)
        
        # Parse table statistics
        elif current_table:
            if 'Active prefixes:' in line_stripped:
                active_match = re.search(r'Active prefixes:\s+(\d+)', line_stripped)
                if active_match:
                    current_table.active_prefixes = int(active_match.group(1))
            
            elif 'Received prefixes:' in line_stripped:
                recv_match = re.search(r'Received prefixes:\s+(\d+)', line_stripped)
                if recv_match:
                    current_table.received_prefixes = int(recv_match.group(1))
            
            elif 'Accepted prefixes:' in line_stripped:
                accept_match = re.search(r'Accepted prefixes:\s+(\d+)', line_stripped)
                if accept_match:
                    current_table.accepted_prefixes = int(accept_match.group(1))
            
            elif 'Advertised prefixes:' in line_stripped:
                adv_match = re.search(r'Advertised prefixes:\s+(\d+)', line_stripped)
                if adv_match:
                    current_table.advertised_prefixes = int(adv_match.group(1))
    
    # Don't forget last neighbor
    if current_neighbor:
        bgp_neighbor.neighbors.append(current_neighbor)
    
    return bgp_neighbor


# ========================================
# show isis adjacency extensive | no-more
# ========================================

def parse_show_isis_adjacency_extensive(cli_output: str) -> ShowIsisAdjacencyExtensive:
    """
    Parse 'show isis adjacency extensive | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowIsisAdjacencyExtensive object with parsed ISIS adjacency information
    """
    
    return _parse_show_isis_adjacency_extensive_regex(cli_output)


def _parse_show_isis_adjacency_extensive_regex(cli_output: str) -> ShowIsisAdjacencyExtensive:
    """Regex-based parser for ISIS adjacency extensive output"""
    isis_adj = ShowIsisAdjacencyExtensive()
    
    lines = cli_output.split('\n')
    current_entry = None
    in_transition_log = False
    
    for line in lines:
        line_stripped = line.strip()
        
        # Check if this is a system name (new entry)
        if line and not line.startswith(' ') and line_stripped and not ':' in line_stripped:
            if current_entry:
                isis_adj.entries.append(current_entry)
            
            current_entry = ShowIsisAdjacencyEntry(
                system_name=line_stripped,
                interface="", level="", state="", expires_in="",
                priority="", up_down_transitions=0, last_transition="",
                circuit_type="", speaks="", topologies="",
                restart_capable="", adjacency_advertisement=""
            )
            in_transition_log = False
            continue
        
        if not current_entry:
            continue
        
        # Parse interface line
        if line_stripped.startswith('Interface:'):
            interface_match = re.search(r'Interface:\s+(\S+),\s+Level:\s+(\d+),\s+State:\s+(\S+),\s+Expires in\s+(.+)', line_stripped)
            if interface_match:
                current_entry.interface = interface_match.group(1)
                current_entry.level = interface_match.group(2)
                current_entry.state = interface_match.group(3)
                current_entry.expires_in = interface_match.group(4)
        
        # Parse priority line
        elif line_stripped.startswith('Priority:'):
            priority_match = re.search(r'Priority:\s+(\d+),\s+Up/Down transitions:\s+(\d+),\s+Last transition:\s+(.+)', line_stripped)
            if priority_match:
                current_entry.priority = priority_match.group(1)
                current_entry.up_down_transitions = int(priority_match.group(2))
                current_entry.last_transition = priority_match.group(3)
        
        # Parse IP addresses
        elif line_stripped.startswith('IP addresses:'):
            ips = line_stripped.split(':', 1)[1].strip().split()
            current_entry.ip_addresses.extend(ips)
        
        # Parse Adj-SID
        elif 'Adj-SID:' in line_stripped:
            adj_sid_match = re.search(r'Adj-SID:\s+(\d+),\s+Flags:\s+(\S+)', line_stripped)
            if adj_sid_match:
                current_entry.adj_sids.append({
                    "sid": adj_sid_match.group(1),
                    "flags": adj_sid_match.group(2)
                })
        
        # Parse transition log header
        elif line_stripped.startswith('Transition log:'):
            in_transition_log = True
        
        # Parse transition log entries
        elif in_transition_log and line_stripped.startswith('When'):
            continue  # Skip header
        
        elif in_transition_log and line_stripped:
            trans_parts = line_stripped.split(None, 3)
            if len(trans_parts) >= 3:
                transition = ShowIsisAdjacencyTransition(
                    when=' '.join(trans_parts[:3]),
                    state=trans_parts[3] if len(trans_parts) > 3 else "",
                    event="",
                    down_reason=""
                )
                # Try to parse state/event/reason
                if len(trans_parts) > 3:
                    remaining = trans_parts[3]
                    parts = remaining.split(None, 2)
                    if len(parts) >= 1:
                        transition.state = parts[0]
                    if len(parts) >= 2:
                        transition.event = parts[1]
                    if len(parts) >= 3:
                        transition.down_reason = parts[2]
                
                current_entry.transition_log.append(transition)
    
    # Don't forget last entry
    if current_entry:
        isis_adj.entries.append(current_entry)
    
    return isis_adj


# ========================================
# show route summary | no-more
# ========================================

def parse_show_route_summary(cli_output: str) -> ShowRouteSummary:
    """
    Parse 'show route summary | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowRouteSummary object with parsed route summary
    """
    
    return _parse_show_route_summary_regex(cli_output)


def _parse_show_route_summary_regex(cli_output: str) -> ShowRouteSummary:
    """Regex-based parser for route summary output"""
    route_summary = ShowRouteSummary()
    
    lines = cli_output.split('\n')
    current_table = None
    
    for line in lines:
        line_stripped = line.strip()
        
        # Parse AS number
        if line_stripped.startswith('Autonomous system number:'):
            route_summary.autonomous_system = line_stripped.split(':', 1)[1].strip()
        
        # Parse Router ID
        elif line_stripped.startswith('Router ID:'):
            route_summary.router_id = line_stripped.split(':', 1)[1].strip()
        
        # Parse table header
        table_match = re.match(r'^(\S+):\s+(\d+)\s+destinations,\s+(\d+)\s+routes\s+\((\d+)\s+active,\s+(\d+)\s+holddown,\s+(\d+)\s+hidden\)', line_stripped)
        if table_match:
            if current_table:
                route_summary.tables.append(current_table)
            
            current_table = ShowRouteSummaryTable(
                table_name=table_match.group(1),
                destinations=int(table_match.group(2)),
                routes=int(table_match.group(3)),
                active=int(table_match.group(4)),
                holddown=int(table_match.group(5)),
                hidden=int(table_match.group(6))
            )
        
        # Parse protocol statistics
        elif current_table:
            protocol_match = re.match(r'^([A-Z][A-Za-z0-9-]+):\s+(\d+)\s+routes?,\s+(\d+)\s+active', line_stripped)
            if protocol_match:
                protocol = ShowRouteSummaryProtocol(
                    protocol=protocol_match.group(1),
                    routes=int(protocol_match.group(2)),
                    active=int(protocol_match.group(3))
                )
                current_table.protocols.append(protocol)
    
    # Don't forget last table
    if current_table:
        route_summary.tables.append(current_table)
    
    return route_summary
# ========================================
# show rsvp session match dn | no-more (17)
# ========================================

def parse_show_rsvp_session_match_dn(cli_output: str) -> ShowRsvpSession:
    """
    Parse 'show rsvp session match dn | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowRsvpSession object with parsed RSVP session entries
    """
    
    # Check if output is None or empty
    if not cli_output or cli_output.strip() == "" or cli_output.strip().lower() == "none":
        return ShowRsvpSession()
    
    # Reuse existing parser since format is identical
    return _parse_show_rsvp_session_regex(cli_output)


# ========================================
# show mpls lsp unidirectional match dn | no-more (18)
# ========================================

def parse_show_mpls_lsp_unidirectional_match_dn(cli_output: str) -> ShowMplsLsp:
    """
    Parse 'show mpls lsp unidirectional match dn | no-more' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowMplsLsp object with parsed MPLS LSP entries
    """
    
    # Check if output is None or empty
    if not cli_output or cli_output.strip() == "" or cli_output.strip().lower() == "none":
        return ShowMplsLsp()
    
    # Reuse existing parser since format is identical
    return _parse_show_mpls_lsp_regex(cli_output)


# ========================================
# show rsvp session first (19)
# ========================================

def parse_show_rsvp_session_first(cli_output: str) -> ShowRsvpSession:
    """
    Parse 'show rsvp session first' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowRsvpSession object with parsed RSVP session entries
    """
    
    # Check if output is None or empty
    if not cli_output or cli_output.strip() == "" or cli_output.strip().lower() == "none":
        return ShowRsvpSession()
    
    # Reuse existing parser since format is identical
    return _parse_show_rsvp_session_regex(cli_output)


# ========================================
# show rsvp session second (20)
# ========================================

def parse_show_rsvp_session_second(cli_output: str) -> ShowRsvpSession:
    """
    Parse 'show rsvp session second' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowRsvpSession object with parsed RSVP session entries
    """
    
    # Check if output is None or empty
    if not cli_output or cli_output.strip() == "" or cli_output.strip().lower() == "none":
        return ShowRsvpSession()
    
    # Reuse existing parser since format is identical
    return _parse_show_rsvp_session_regex(cli_output)


# ========================================
# show rsvp session ma (21)
# ========================================

def parse_show_rsvp_session_ma(cli_output: str) -> ShowRsvpSession:
    """
    Parse 'show rsvp session ma' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowRsvpSession object with parsed RSVP session entries
    """
    
    # Check if output is None or empty
    if not cli_output or cli_output.strip() == "" or cli_output.strip().lower() == "none":
        return ShowRsvpSession()
    
    # Reuse existing parser since format is identical
    return _parse_show_rsvp_session_regex(cli_output)


# ========================================
# show mpls lsp unidirectional (22)
# ========================================

def parse_show_mpls_lsp_unidirectional(cli_output: str) -> ShowMplsLsp:
    """
    Parse 'show mpls lsp unidirectional' output
    
    Args:
        cli_output: Raw CLI output string from command segmenter
        
    Returns:
        ShowMplsLsp object with parsed MPLS LSP entries
    """
    
    # Check if output is None or empty
    if not cli_output or cli_output.strip() == "" or cli_output.strip().lower() == "none":
        return ShowMplsLsp()
    
    # Reuse existing parser since format is identical
    return _parse_show_mpls_lsp_regex(cli_output)

# ========================================
# Main execution - Testing all commands 1-22
# ========================================
if __name__ == "__main__":
    
    raw_output = read_mx80_show_commands("pre_check.txt")
    
    # # Test command 1: show arp no-resolve
    # print("=" * 70)
    # print("Command 1: show arp no-resolve | no-more")
    # print("=" * 70)
    # output_1 = extract_show_arp_output_1(raw_output)
    # result_1 = parse_show_arp_no_resolve(output_1)
    # print(json.dumps(result_1.to_dict(), indent=2))
    # print("\n✓ Command 1 completed\n")
    
    # # Test command 2: show vrrp summary
    # print("=" * 70)
    # print("Command 2: show vrrp summary | no-more")
    # print("=" * 70)
    # output_2 = extract_show_vrrp_summary_output_2(raw_output)
    # result_2 = parse_show_vrrp_summary(output_2)
    # print(json.dumps(result_2.to_dict(), indent=2))
    # print("\n✓ Command 2 completed\n")
    
    # # Test command 3: show lldp neighbors
    # print("=" * 70)
    # print("Command 3: show lldp neighbors | no-more")
    # print("=" * 70)
    # output_3 = extract_show_lldp_neighbors_output_3(raw_output)
    # result_3 = parse_show_lldp_neighbors(output_3)
    # print(json.dumps(result_3.to_dict(), indent=2))
    # print("\n✓ Command 3 completed\n")
    
    # # Test command 4: show bfd session
    # print("=" * 70)
    # print("Command 4: show bfd session | no-more")
    # print("=" * 70)
    # output_4 = extract_show_bfd_session_output_4(raw_output)
    # result_4 = parse_show_bfd_session(output_4)
    # print(json.dumps(result_4.to_dict(), indent=2))
    # print("\n✓ Command 4 completed\n")
    
    # # Test command 5: show rsvp neighbor
    # print("=" * 70)
    # print("Command 5: show rsvp neighbor | no-more")
    # print("=" * 70)
    # output_5 = extract_show_rsvp_neighbor_output_5(raw_output)
    # result_5 = parse_show_rsvp_neighbor(output_5)
    # print(json.dumps(result_5.to_dict(), indent=2))
    # print("\n✓ Command 5 completed\n")
    
    # # Test command 6: show rsvp session
    # print("=" * 70)
    # print("Command 6: show rsvp session | no-more")
    # print("=" * 70)
    # output_6 = extract_show_rsvp_session_output_6(raw_output)
    # result_6 = parse_show_rsvp_session(output_6)
    # print(json.dumps(result_6.to_dict(), indent=2))
    # print("\n✓ Command 6 completed\n")
    
    # # Test command 7: show route table inet.0
    # print("=" * 70)
    # print("Command 7: show route table inet.0 | no-more")
    # print("=" * 70)
    # output_7 = extract_show_route_table_inet0_output_7(raw_output)
    # result_7 = parse_show_route_table_inet0(output_7)
    # print(json.dumps(result_7.to_dict(), indent=2))
    # print("\n✓ Command 7 completed\n")
    
    # # Test command 8: show route table inet.3
    # print("=" * 70)
    # print("Command 8: show route table inet.3 | no-more")
    # print("=" * 70)
    # output_8 = extract_show_route_table_inet3_output_8(raw_output)
    # result_8 = parse_show_route_table_inet3(output_8)
    # print(json.dumps(result_8.to_dict(), indent=2))
    # print("\n✓ Command 8 completed\n")
    
    # # Test command 9: show route table mpls.0
    # print("=" * 70)
    # print("Command 9: show route table mpls.0 | no-more")
    # print("=" * 70)
    # output_9 = extract_show_route_table_mpls0_output_9(raw_output)
    # result_9 = parse_show_route_table_mpls0(output_9)
    # print(json.dumps(result_9.to_dict(), indent=2))
    # print("\n✓ Command 9 completed\n")
    
    # # Test command 10: show mpls interface
    # print("=" * 70)
    # print("Command 10: show mpls interface | no-more")
    # print("=" * 70)
    # output_10 = extract_show_mpls_interface_output_10(raw_output)
    # result_10 = parse_show_mpls_interface(output_10)
    # print(json.dumps(result_10.to_dict(), indent=2))
    # print("\n✓ Command 10 completed\n")
    
    # # Test command 11: show mpls lsp
    # print("=" * 70)
    # print("Command 11: show mpls lsp | no-more")
    # print("=" * 70)
    # output_11 = extract_show_mpls_lsp_output_11(raw_output)
    # result_11 = parse_show_mpls_lsp(output_11)
    # print(json.dumps(result_11.to_dict(), indent=2))
    # print("\n✓ Command 11 completed\n")
    
    # # Test command 12: show mpls lsp p2mp
    # print("=" * 70)
    # print("Command 12: show mpls lsp p2mp | no-more")
    # print("=" * 70)
    # output_12 = extract_show_mpls_lsp_p2mp_output_12(raw_output)
    # result_12 = parse_show_mpls_lsp_p2mp(output_12)
    # print(json.dumps(result_12.to_dict(), indent=2))
    # print("\n✓ Command 12 completed\n")
    
    # # Test command 13: show bgp summary
    # print("=" * 70)
    # print("Command 13: show bgp summary | no-more")
    # print("=" * 70)
    # output_13 = extract_show_bgp_summary_output_13(raw_output)
    # result_13 = parse_show_bgp_summary(output_13)
    # print(json.dumps(result_13.to_dict(), indent=2))
    # print("\n✓ Command 13 completed\n")
    
    # # Test command 14: show bgp neighbor
    # print("=" * 70)
    # print("Command 14: show bgp neighbor | no-more")
    # print("=" * 70)
    # output_14 = extract_show_bgp_neighbor_output_14(raw_output)
    # result_14 = parse_show_bgp_neighbor(output_14)
    # print(json.dumps(result_14.to_dict(), indent=2))
    # print("\n✓ Command 14 completed\n")
    
    # # Test command 15: show isis adjacency extensive
    # print("=" * 70)
    # print("Command 15: show isis adjacency extensive | no-more")
    # print("=" * 70)
    # output_15 = extract_show_isis_adjacency_extensive_output_15(raw_output)
    # result_15 = parse_show_isis_adjacency_extensive(output_15)
    # print(json.dumps(result_15.to_dict(), indent=2))
    # print("\n✓ Command 15 completed\n")
    
    # # Test command 16: show route summary
    # print("=" * 70)
    # print("Command 16: show route summary | no-more")
    # print("=" * 70)
    # output_16 = extract_show_route_summary_output_16(raw_output)
    # result_16 = parse_show_route_summary(output_16)
    # print(json.dumps(result_16.to_dict(), indent=2))
    # print("\n✓ Command 16 completed\n")
    
    # # Test command 17: show rsvp session match dn
    # print("=" * 70)
    # print("Command 17: show rsvp session match dn | no-more")
    # print("=" * 70)
    # output_17 = extract_show_rsvp_session_match_dn_output_17(raw_output)
    # result_17 = parse_show_rsvp_session_match_dn(output_17)
    # print(json.dumps(result_17.to_dict(), indent=2))
    # print("\n✓ Command 17 completed\n")
    
    # # Test command 18: show mpls lsp unidirectional match dn
    # print("=" * 70)
    # print("Command 18: show mpls lsp unidirectional match dn | no-more")
    # print("=" * 70)
    # output_18 = extract_show_mpls_lsp_unidirectional_match_dn_output_18(raw_output)
    # result_18 = parse_show_mpls_lsp_unidirectional_match_dn(output_18)
    # print(json.dumps(result_18.to_dict(), indent=2))
    # print("\n✓ Command 18 completed\n")
    
    # # Test command 19: show rsvp session first
    # print("=" * 70)
    # print("Command 19: show rsvp session first")
    # print("=" * 70)
    # output_19 = extract_show_rsvp_session_first_output_19(raw_output)
    # result_19 = parse_show_rsvp_session_first(output_19)
    # print(json.dumps(result_19.to_dict(), indent=2))
    # print("\n✓ Command 19 completed\n")
    
    # # Test command 20: show rsvp session second
    # print("=" * 70)
    # print("Command 20: show rsvp session second")
    # print("=" * 70)
    # output_20 = extract_show_rsvp_session_second_output_20(raw_output)
    # result_20 = parse_show_rsvp_session_second(output_20)
    # print(json.dumps(result_20.to_dict(), indent=2))
    # print("\n✓ Command 20 completed\n")
    
    # # Test command 21: show rsvp session ma
    # print("=" * 70)
    # print("Command 21: show rsvp session ma")
    # print("=" * 70)
    # output_21 = extract_show_rsvp_session_ma_output_21(raw_output)
    # result_21 = parse_show_rsvp_session_ma(output_21)
    # print(json.dumps(result_21.to_dict(), indent=2))
    # print("\n✓ Command 21 completed\n")
    
    # # Test command 22: show mpls lsp unidirectional
    # print("=" * 70)
    # print("Command 22: show mpls lsp unidirectional")
    # print("=" * 70)
    # output_22 = extract_show_mpls_lsp_unidirectional_output_22(raw_output)
    # result_22 = parse_show_mpls_lsp_unidirectional(output_22)
    # print(json.dumps(result_22.to_dict(), indent=2))
    # print("\n✓ Command 22 completed\n")
    
    # print("=" * 70)
    # print("ALL COMMANDS COMPLETED SUCCESSFULLY (1-22)")
    # print("=" * 70)