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
    ShowVrrpSummary, ShowVrrpSummaryEntry, ShowVrrpSummaryAddress
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
# Main execution
# ========================================

if __name__ == "__main__":
    import json
    from command_segmenter import (
        read_mx80_show_commands, 
        extract_show_arp_output,
        extract_show_vrrp_summary_output
    )
    
    raw_output = read_mx80_show_commands()
    
    # Test show arp no-resolve
    print("=" * 50)
    print("show arp no-resolve | no-more")
    print("=" * 50)
    arp_output = extract_show_arp_output(raw_output)
    arp_result = parse_show_arp_no_resolve(arp_output)
    print(json.dumps(arp_result.to_dict(), indent=2))
    
    # Test show vrrp summary
    print("\n" + "=" * 50)
    print("show vrrp summary | no-more")
    print("=" * 50)
    vrrp_output = extract_show_vrrp_summary_output(raw_output)
    vrrp_result = parse_show_vrrp_summary(vrrp_output)
    print(json.dumps(vrrp_result.to_dict(), indent=2))