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

# ========================================
# show lldp neighbors | no-more
# ========================================
@dataclass
class ShowLldpNeighborsEntry:
    """Represents a single LLDP neighbor entry"""
    local_interface: str
    parent_interface: str
    chassis_id: str
    port_info: str
    system_name: str

@dataclass
class ShowLldpNeighbors:
    """Represents the complete LLDP neighbors output"""
    entries: List[ShowLldpNeighborsEntry] = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "entries": [
                {
                    "local_interface": entry.local_interface,
                    "parent_interface": entry.parent_interface,
                    "chassis_id": entry.chassis_id,
                    "port_info": entry.port_info,
                    "system_name": entry.system_name
                }
                for entry in self.entries
            ]
        }

# ========================================
# show bfd session | no-more
# ========================================
@dataclass
class ShowBfdSessionEntry:
    """Represents a single BFD session entry"""
    address: str
    state: str
    interface: str
    detect_time: str
    transmit_interval: str
    multiplier: str

@dataclass
class ShowBfdSession:
    """Represents the complete BFD session output"""
    entries: List[ShowBfdSessionEntry] = field(default_factory=list)
    total_sessions: int = 0
    total_clients: int = 0
    cumulative_transmit_rate: str = ""
    cumulative_receive_rate: str = ""
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "total_sessions": self.total_sessions,
            "total_clients": self.total_clients,
            "cumulative_transmit_rate": self.cumulative_transmit_rate,
            "cumulative_receive_rate": self.cumulative_receive_rate,
            "entries": [
                {
                    "address": entry.address,
                    "state": entry.state,
                    "interface": entry.interface,
                    "detect_time": entry.detect_time,
                    "transmit_interval": entry.transmit_interval,
                    "multiplier": entry.multiplier
                }
                for entry in self.entries
            ]
        }

# ========================================
# show rsvp neighbor | no-more
# ========================================
@dataclass
class ShowRsvpNeighborEntry:
    """Represents a single RSVP neighbor entry"""
    address: str
    idle: str
    up_dn: str
    last_change: str
    hello_interval: str
    hello_tx_rx: str
    msg_rcvd: str

@dataclass
class ShowRsvpNeighbor:
    """Represents the complete RSVP neighbor output"""
    entries: List[ShowRsvpNeighborEntry] = field(default_factory=list)
    total_neighbors: int = 0
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "total_neighbors": self.total_neighbors,
            "entries": [
                {
                    "address": entry.address,
                    "idle": entry.idle,
                    "up_dn": entry.up_dn,
                    "last_change": entry.last_change,
                    "hello_interval": entry.hello_interval,
                    "hello_tx_rx": entry.hello_tx_rx,
                    "msg_rcvd": entry.msg_rcvd
                }
                for entry in self.entries
            ]
        }