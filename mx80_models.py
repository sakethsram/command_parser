"""
Data models for Juniper MX80 CLI parsing
Defines the structure of parsed command outputs
"""

from typing import List, Optional
from dataclasses import dataclass, field


# ========================================
# show arp no-resolve | no-more
# ========================================

@dataclass
class ShowArpNoResolveEntry:
    """Represents a single ARP table entry"""
    mac_address: str
    ip_address: str
    interface: str
    flags: str


@dataclass
class ShowArpNoResolve:
    """Represents the complete ARP table output"""
    entries: List[ShowArpNoResolveEntry] = field(default_factory=list)
    total_entries: int = 0
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "total_entries": self.total_entries,
            "entries": [
                {
                    "mac_address": entry.mac_address,
                    "ip_address": entry.ip_address,
                    "interface": entry.interface,
                    "flags": entry.flags
                }
                for entry in self.entries
            ]
        }


# ========================================
# show vrrp summary | no-more
# ========================================

@dataclass
class ShowVrrpSummaryAddress:
    """Represents a VRRP address (lcl or vip)"""
    type: str  # 'lcl' or 'vip'
    address: str


@dataclass
class ShowVrrpSummaryEntry:
    """Represents a single VRRP group entry"""
    interface: str
    state: str
    group: int
    vr_state: str
    vr_mode: str
    addresses: List[ShowVrrpSummaryAddress] = field(default_factory=list)


@dataclass
class ShowVrrpSummary:
    """Represents the complete VRRP summary output"""
    entries: List[ShowVrrpSummaryEntry] = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "entries": [
                {
                    "interface": entry.interface,
                    "state": entry.state,
                    "group": entry.group,
                    "vr_state": entry.vr_state,
                    "vr_mode": entry.vr_mode,
                    "addresses": [
                        {
                            "type": addr.type,
                            "address": addr.address
                        }
                        for addr in entry.addresses
                    ]
                }
                for entry in self.entries
            ]
        }