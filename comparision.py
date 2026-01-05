import json
import re
from typing import Optional, Dict, Any
from genie.conf.base import Device
from genie.libs.parser.junos.show_arp import ShowArpNoResolve as GenieShowArpNoResolve
from mx80_models import (
    ShowArpNoResolve, ShowArpNoResolveEntry,
    ShowVrrpSummary, ShowVrrpSummaryEntry, ShowVrrpSummaryAddress
)
import json
from command_segmenter import (
        read_mx80_show_commands, 
        extract_show_arp_output,
        extract_show_vrrp_summary_output
    )
from mx80_parser_engine import *
def wrapper(file_path):
    raw_output=read_mx80_show_commands(file_path)

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

wrapper("post_update.txt")
