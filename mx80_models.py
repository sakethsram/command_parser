"""
Data models for Juniper MX80 CLI parsing
Defines the structure of parsed command outputs
"""
from typing import List, Optional, Dict

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
    # ========================================
# show rsvp session | no-more
# ========================================
@dataclass
class ShowRsvpSessionEntry:
    """Represents a single RSVP session entry"""
    to: str
    from_addr: str
    state: str
    rt: str
    style: str
    labelin: str
    labelout: str
    lspname: str

@dataclass
class ShowRsvpSessionSection:
    """Represents a section of RSVP sessions (Ingress/Egress/Transit)"""
    section_type: str  # 'Ingress', 'Egress', or 'Transit'
    total_sessions: int
    entries: List[ShowRsvpSessionEntry] = field(default_factory=list)
    total_displayed: int = 0
    total_up: int = 0
    total_down: int = 0

@dataclass
class ShowRsvpSession:
    """Represents the complete RSVP session output"""
    ingress: Optional[ShowRsvpSessionSection] = None
    egress: Optional[ShowRsvpSessionSection] = None
    transit: Optional[ShowRsvpSessionSection] = None
    
    def to_dict(self):
        """Convert to dictionary format"""
        result = {}
        
        if self.ingress:
            result["ingress"] = {
                "section_type": self.ingress.section_type,
                "total_sessions": self.ingress.total_sessions,
                "total_displayed": self.ingress.total_displayed,
                "total_up": self.ingress.total_up,
                "total_down": self.ingress.total_down,
                "entries": [
                    {
                        "to": entry.to,
                        "from": entry.from_addr,
                        "state": entry.state,
                        "rt": entry.rt,
                        "style": entry.style,
                        "labelin": entry.labelin,
                        "labelout": entry.labelout,
                        "lspname": entry.lspname
                    }
                    for entry in self.ingress.entries
                ]
            }
        
        if self.egress:
            result["egress"] = {
                "section_type": self.egress.section_type,
                "total_sessions": self.egress.total_sessions,
                "total_displayed": self.egress.total_displayed,
                "total_up": self.egress.total_up,
                "total_down": self.egress.total_down,
                "entries": [
                    {
                        "to": entry.to,
                        "from": entry.from_addr,
                        "state": entry.state,
                        "rt": entry.rt,
                        "style": entry.style,
                        "labelin": entry.labelin,
                        "labelout": entry.labelout,
                        "lspname": entry.lspname
                    }
                    for entry in self.egress.entries
                ]
            }
        
        if self.transit:
            result["transit"] = {
                "section_type": self.transit.section_type,
                "total_sessions": self.transit.total_sessions,
                "total_displayed": self.transit.total_displayed,
                "total_up": self.transit.total_up,
                "total_down": self.transit.total_down,
                "entries": [
                    {
                        "to": entry.to,
                        "from": entry.from_addr,
                        "state": entry.state,
                        "rt": entry.rt,
                        "style": entry.style,
                        "labelin": entry.labelin,
                        "labelout": entry.labelout,
                        "lspname": entry.lspname
                    }
                    for entry in self.transit.entries
                ]
            }
        
        return result


# ========================================
# show route table inet.0 | no-more
# ========================================
@dataclass
class ShowRouteTableInet0Entry:
    """Represents a single route entry"""
    destination: str
    protocol: str
    preference: str
    metric: str
    age: str
    next_hop: str
    via: str
    mpls_label: str = ""  # Optional MPLS label info like "Push 163028"

@dataclass
class ShowRouteTableInet0:
    """Represents the complete inet.0 routing table output"""
    total_destinations: int = 0
    total_routes: int = 0
    active_routes: int = 0
    holddown_routes: int = 0
    hidden_routes: int = 0
    entries: List[ShowRouteTableInet0Entry] = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "total_destinations": self.total_destinations,
            "total_routes": self.total_routes,
            "active_routes": self.active_routes,
            "holddown_routes": self.holddown_routes,
            "hidden_routes": self.hidden_routes,
            "entries": [
                {
                    "destination": entry.destination,
                    "protocol": entry.protocol,
                    "preference": entry.preference,
                    "metric": entry.metric,
                    "age": entry.age,
                    "next_hop": entry.next_hop,
                    "via": entry.via,
                    "mpls_label": entry.mpls_label
                }
                for entry in self.entries
            ]
        }


# ========================================
# show route table inet.3 | no-more
# ========================================
@dataclass
class ShowRouteTableInet3NextHop:
    """Represents a single next-hop for a route"""
    to: str
    via: str
    mpls_label: str = ""

@dataclass
class ShowRouteTableInet3Entry:
    """Represents a single route entry with multiple next-hops"""
    destination: str
    protocol: str
    preference: str
    metric: str
    age: str
    next_hops: List[ShowRouteTableInet3NextHop] = field(default_factory=list)

@dataclass
class ShowRouteTableInet3:
    """Represents the complete inet.3 routing table output"""
    total_destinations: int = 0
    total_routes: int = 0
    active_routes: int = 0
    holddown_routes: int = 0
    hidden_routes: int = 0
    entries: List[ShowRouteTableInet3Entry] = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "total_destinations": self.total_destinations,
            "total_routes": self.total_routes,
            "active_routes": self.active_routes,
            "holddown_routes": self.holddown_routes,
            "hidden_routes": self.hidden_routes,
            "entries": [
                {
                    "destination": entry.destination,
                    "protocol": entry.protocol,
                    "preference": entry.preference,
                    "metric": entry.metric,
                    "age": entry.age,
                    "next_hops": [
                        {
                            "to": nh.to,
                            "via": nh.via,
                            "mpls_label": nh.mpls_label
                        }
                        for nh in entry.next_hops
                    ]
                }
                for entry in self.entries
            ]
        }


# ========================================
# show route table mpls.0 | no-more
# ========================================
@dataclass
class ShowRouteTableMpls0NextHop:
    """Represents a single next-hop for an MPLS route"""
    to: str = ""
    via: str = ""
    mpls_label: str = ""
    lsp_name: str = ""
    action: str = ""  # Pop, Swap, Push, Receive, Discard, etc.

@dataclass
class ShowRouteTableMpls0Entry:
    """Represents a single MPLS route entry"""
    label: str
    protocol: str
    preference: str
    metric: str
    age: str
    next_hops: List[ShowRouteTableMpls0NextHop] = field(default_factory=list)

@dataclass
class ShowRouteTableMpls0:
    """Represents the complete mpls.0 routing table output"""
    total_destinations: int = 0
    total_routes: int = 0
    active_routes: int = 0
    holddown_routes: int = 0
    hidden_routes: int = 0
    entries: List[ShowRouteTableMpls0Entry] = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "total_destinations": self.total_destinations,
            "total_routes": self.total_routes,
            "active_routes": self.active_routes,
            "holddown_routes": self.holddown_routes,
            "hidden_routes": self.hidden_routes,
            "entries": [
                {
                    "label": entry.label,
                    "protocol": entry.protocol,
                    "preference": entry.preference,
                    "metric": entry.metric,
                    "age": entry.age,
                    "next_hops": [
                        {
                            "to": nh.to,
                            "via": nh.via,
                            "mpls_label": nh.mpls_label,
                            "lsp_name": nh.lsp_name,
                            "action": nh.action
                        }
                        for nh in entry.next_hops
                    ]
                }
                for entry in self.entries
            ]
        }

# ========================================
# show mpls interface | no-more
# ========================================
@dataclass
class ShowMplsInterfaceEntry:
    """Represents a single MPLS interface entry"""
    interface: str
    state: str
    administrative_groups: str

@dataclass
class ShowMplsInterface:
    """Represents the complete MPLS interface output"""
    entries: List[ShowMplsInterfaceEntry] = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "entries": [
                {
                    "interface": entry.interface,
                    "state": entry.state,
                    "administrative_groups": entry.administrative_groups
                }
                for entry in self.entries
            ]
        }


# ========================================
# show mpls lsp | no-more
# ========================================
@dataclass
class ShowMplsLspEntry:
    """Represents a single MPLS LSP entry"""
    to: str
    from_addr: str
    state: str
    rt: str
    p: str
    active_path: str
    style: str = ""
    labelin: str = ""
    labelout: str = ""
    lspname: str = ""

@dataclass
class ShowMplsLspSection:
    """Represents a section of MPLS LSPs (Ingress/Egress/Transit)"""
    section_type: str  # 'Ingress', 'Egress', or 'Transit'
    total_sessions: int
    entries: List[ShowMplsLspEntry] = field(default_factory=list)
    total_displayed: int = 0
    total_up: int = 0
    total_down: int = 0

@dataclass
class ShowMplsLsp:
    """Represents the complete MPLS LSP output"""
    ingress: Optional[ShowMplsLspSection] = None
    egress: Optional[ShowMplsLspSection] = None
    transit: Optional[ShowMplsLspSection] = None
    
    def to_dict(self):
        """Convert to dictionary format"""
        result = {}
        
        if self.ingress:
            result["ingress"] = {
                "section_type": self.ingress.section_type,
                "total_sessions": self.ingress.total_sessions,
                "total_displayed": self.ingress.total_displayed,
                "total_up": self.ingress.total_up,
                "total_down": self.ingress.total_down,
                "entries": [
                    {
                        "to": entry.to,
                        "from": entry.from_addr,
                        "state": entry.state,
                        "rt": entry.rt,
                        "p": entry.p,
                        "active_path": entry.active_path,
                        "style": entry.style,
                        "labelin": entry.labelin,
                        "labelout": entry.labelout,
                        "lspname": entry.lspname
                    }
                    for entry in self.ingress.entries
                ]
            }
        
        if self.egress:
            result["egress"] = {
                "section_type": self.egress.section_type,
                "total_sessions": self.egress.total_sessions,
                "total_displayed": self.egress.total_displayed,
                "total_up": self.egress.total_up,
                "total_down": self.egress.total_down,
                "entries": [
                    {
                        "to": entry.to,
                        "from": entry.from_addr,
                        "state": entry.state,
                        "rt": entry.rt,
                        "p": entry.p,
                        "active_path": entry.active_path,
                        "style": entry.style,
                        "labelin": entry.labelin,
                        "labelout": entry.labelout,
                        "lspname": entry.lspname
                    }
                    for entry in self.egress.entries
                ]
            }
        
        if self.transit:
            result["transit"] = {
                "section_type": self.transit.section_type,
                "total_sessions": self.transit.total_sessions,
                "total_displayed": self.transit.total_displayed,
                "total_up": self.transit.total_up,
                "total_down": self.transit.total_down,
                "entries": [
                    {
                        "to": entry.to,
                        "from": entry.from_addr,
                        "state": entry.state,
                        "rt": entry.rt,
                        "p": entry.p,
                        "active_path": entry.active_path,
                        "style": entry.style,
                        "labelin": entry.labelin,
                        "labelout": entry.labelout,
                        "lspname": entry.lspname
                    }
                    for entry in self.transit.entries
                ]
            }
        
        return result


# ========================================
# show mpls lsp p2mp | no-more
# ========================================
@dataclass
class ShowMplsLspP2mpEntry:
    """Represents a single P2MP LSP entry"""
    to: str
    from_addr: str
    state: str
    rt: str
    p: str = ""
    active_path: str = ""
    style: str = ""
    labelin: str = ""
    labelout: str = ""
    lspname: str = ""

@dataclass
class ShowMplsLspP2mpGroup:
    """Represents a P2MP group with its name, branch count, and entries"""
    p2mp_name: str
    branch_count: int
    entries: List[ShowMplsLspP2mpEntry] = field(default_factory=list)

@dataclass
class ShowMplsLspP2mpSection:
    """Represents a section of P2MP LSPs (Ingress/Egress/Transit)"""
    section_type: str  # 'Ingress', 'Egress', or 'Transit'
    total_sessions: int
    groups: List[ShowMplsLspP2mpGroup] = field(default_factory=list)
    total_displayed: int = 0
    total_up: int = 0
    total_down: int = 0

@dataclass
class ShowMplsLspP2mp:
    """Represents the complete MPLS LSP P2MP output"""
    ingress: Optional[ShowMplsLspP2mpSection] = None
    egress: Optional[ShowMplsLspP2mpSection] = None
    transit: Optional[ShowMplsLspP2mpSection] = None
    
    def to_dict(self):
        """Convert to dictionary format"""
        result = {}
        
        if self.ingress:
            result["ingress"] = {
                "section_type": self.ingress.section_type,
                "total_sessions": self.ingress.total_sessions,
                "total_displayed": self.ingress.total_displayed,
                "total_up": self.ingress.total_up,
                "total_down": self.ingress.total_down,
                "groups": [
                    {
                        "p2mp_name": group.p2mp_name,
                        "branch_count": group.branch_count,
                        "entries": [
                            {
                                "to": entry.to,
                                "from": entry.from_addr,
                                "state": entry.state,
                                "rt": entry.rt,
                                "p": entry.p,
                                "active_path": entry.active_path,
                                "style": entry.style,
                                "labelin": entry.labelin,
                                "labelout": entry.labelout,
                                "lspname": entry.lspname
                            }
                            for entry in group.entries
                        ]
                    }
                    for group in self.ingress.groups
                ]
            }
        
        if self.egress:
            result["egress"] = {
                "section_type": self.egress.section_type,
                "total_sessions": self.egress.total_sessions,
                "total_displayed": self.egress.total_displayed,
                "total_up": self.egress.total_up,
                "total_down": self.egress.total_down,
                "groups": [
                    {
                        "p2mp_name": group.p2mp_name,
                        "branch_count": group.branch_count,
                        "entries": [
                            {
                                "to": entry.to,
                                "from": entry.from_addr,
                                "state": entry.state,
                                "rt": entry.rt,
                                "p": entry.p,
                                "active_path": entry.active_path,
                                "style": entry.style,
                                "labelin": entry.labelin,
                                "labelout": entry.labelout,
                                "lspname": entry.lspname
                            }
                            for entry in group.entries
                        ]
                    }
                    for group in self.egress.groups
                ]
            }
        
        if self.transit:
            result["transit"] = {
                "section_type": self.transit.section_type,
                "total_sessions": self.transit.total_sessions,
                "total_displayed": self.transit.total_displayed,
                "total_up": self.transit.total_up,
                "total_down": self.transit.total_down,
                "groups": [
                    {
                        "p2mp_name": group.p2mp_name,
                        "branch_count": group.branch_count,
                        "entries": [
                            {
                                "to": entry.to,
                                "from": entry.from_addr,
                                "state": entry.state,
                                "rt": entry.rt,
                                "p": entry.p,
                                "active_path": entry.active_path,
                                "style": entry.style,
                                "labelin": entry.labelin,
                                "labelout": entry.labelout,
                                "lspname": entry.lspname
                            }
                            for entry in group.entries
                        ]
                    }
                    for group in self.transit.groups
                ]
            }
        
        return result
# ========================================
# show bgp summary | no-more
# ========================================
@dataclass
class ShowBgpSummaryTable:
    """Represents routing table statistics"""
    table_name: str
    total_paths: int
    active_paths: int
    suppressed: int
    history: int
    damp_state: int
    pending: int

@dataclass
class ShowBgpSummaryPeerRib:
    """Represents a peer's RIB statistics"""
    table_name: str
    active_received_accepted_damped: str  # Format: "1/4/4/0"

@dataclass
class ShowBgpSummaryPeer:
    """Represents a BGP peer"""
    peer: str
    asn: str
    in_pkt: str
    out_pkt: str
    out_q: str
    flaps: str
    last_up_dwn: str
    state: str
    ribs: List[ShowBgpSummaryPeerRib] = field(default_factory=list)

@dataclass
class ShowBgpSummary:
    """Represents the complete BGP summary output"""
    threading_mode: str = ""
    default_ebgp_mode: str = ""
    groups: int = 0
    peers: int = 0
    down_peers: int = 0
    tables: List[ShowBgpSummaryTable] = field(default_factory=list)
    peer_list: List[ShowBgpSummaryPeer] = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "threading_mode": self.threading_mode,
            "default_ebgp_mode": self.default_ebgp_mode,
            "groups": self.groups,
            "peers": self.peers,
            "down_peers": self.down_peers,
            "tables": [
                {
                    "table_name": table.table_name,
                    "total_paths": table.total_paths,
                    "active_paths": table.active_paths,
                    "suppressed": table.suppressed,
                    "history": table.history,
                    "damp_state": table.damp_state,
                    "pending": table.pending
                }
                for table in self.tables
            ],
            "peer_list": [
                {
                    "peer": peer.peer,
                    "asn": peer.asn,
                    "in_pkt": peer.in_pkt,
                    "out_pkt": peer.out_pkt,
                    "out_q": peer.out_q,
                    "flaps": peer.flaps,
                    "last_up_dwn": peer.last_up_dwn,
                    "state": peer.state,
                    "ribs": [
                        {
                            "table_name": rib.table_name,
                            "active_received_accepted_damped": rib.active_received_accepted_damped
                        }
                        for rib in peer.ribs
                    ]
                }
                for peer in self.peer_list
            ]
        }


# ========================================
# show bgp neighbor | no-more
# ========================================
@dataclass
class ShowBgpNeighborTable:
    """Represents a BGP neighbor's table statistics"""
    table_name: str
    bit: str = ""
    rib_state: List[str] = field(default_factory=list)
    send_state: str = ""
    active_prefixes: int = 0
    received_prefixes: int = 0
    accepted_prefixes: int = 0
    suppressed_damping: int = 0
    advertised_prefixes: int = 0

@dataclass
class ShowBgpNeighborEntry:
    """Represents a single BGP neighbor"""
    peer: str
    peer_as: str
    local: str
    local_as: str
    description: str = ""
    group: str = ""
    routing_instance: str = ""
    forwarding_routing_instance: str = ""
    type: str = ""
    state: str = ""
    flags: str = ""
    last_state: str = ""
    last_event: str = ""
    last_error: str = ""
    export_policy: List[str] = field(default_factory=list)
    import_policy: List[str] = field(default_factory=list)
    options: List[str] = field(default_factory=list)
    authentication_key_configured: bool = False
    address_families: List[str] = field(default_factory=list)
    local_address: str = ""
    holdtime: str = ""
    preference: str = ""
    graceful_shutdown_receiver_local_preference: str = ""
    number_of_flaps: int = 0
    last_flap_event: str = ""
    errors: Dict[str, Dict[str, int]] = field(default_factory=dict)
    peer_id: str = ""
    local_id: str = ""
    active_holdtime: str = ""
    keepalive_interval: str = ""
    group_index: str = ""
    peer_index: str = ""
    snmp_index: str = ""
    io_session_thread: str = ""
    bfd: str = ""
    local_interface: str = ""
    nlri_restart_configured: List[str] = field(default_factory=list)
    nlri_advertised: List[str] = field(default_factory=list)
    nlri_this_session: List[str] = field(default_factory=list)
    peer_capabilities: List[str] = field(default_factory=list)
    tables: List[ShowBgpNeighborTable] = field(default_factory=list)
    last_traffic_received: str = ""
    last_traffic_sent: str = ""
    last_traffic_checked: str = ""
    input_messages: Dict[str, str] = field(default_factory=dict)
    output_messages: Dict[str, str] = field(default_factory=dict)
    output_queues: List[str] = field(default_factory=list)

@dataclass
class ShowBgpNeighbor:
    """Represents the complete BGP neighbor output"""
    neighbors: List[ShowBgpNeighborEntry] = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "neighbors": [
                {
                    "peer": neighbor.peer,
                    "peer_as": neighbor.peer_as,
                    "local": neighbor.local,
                    "local_as": neighbor.local_as,
                    "description": neighbor.description,
                    "group": neighbor.group,
                    "routing_instance": neighbor.routing_instance,
                    "type": neighbor.type,
                    "state": neighbor.state,
                    "local_address": neighbor.local_address,
                    "holdtime": neighbor.holdtime,
                    "number_of_flaps": neighbor.number_of_flaps,
                    "tables": [
                        {
                            "table_name": table.table_name,
                            "active_prefixes": table.active_prefixes,
                            "received_prefixes": table.received_prefixes,
                            "accepted_prefixes": table.accepted_prefixes,
                            "advertised_prefixes": table.advertised_prefixes
                        }
                        for table in neighbor.tables
                    ]
                }
                for neighbor in self.neighbors
            ]
        }


# ========================================
# show isis adjacency extensive | no-more
# ========================================
@dataclass
class ShowIsisAdjacencyTransition:
    """Represents a single transition log entry"""
    when: str
    state: str
    event: str
    down_reason: str = ""

@dataclass
class ShowIsisAdjacencyEntry:
    """Represents a single ISIS adjacency"""
    system_name: str
    interface: str
    level: str
    state: str
    expires_in: str
    priority: str
    up_down_transitions: int
    last_transition: str
    circuit_type: str
    speaks: str
    topologies: str
    restart_capable: str
    adjacency_advertisement: str
    ip_addresses: List[str] = field(default_factory=list)
    adj_sids: List[Dict[str, str]] = field(default_factory=list)
    transition_log: List[ShowIsisAdjacencyTransition] = field(default_factory=list)

@dataclass
class ShowIsisAdjacencyExtensive:
    """Represents the complete ISIS adjacency extensive output"""
    entries: List[ShowIsisAdjacencyEntry] = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary format"""
        return {
            "entries": [
                {
                    "system_name": entry.system_name,
                    "interface": entry.interface,
                    "level": entry.level,
                    "state": entry.state,
                    "expires_in": entry.expires_in,
                    "up_down_transitions": entry.up_down_transitions,
                    "last_transition": entry.last_transition,
                    "ip_addresses": entry.ip_addresses,
                    "adj_sids": entry.adj_sids,
                    "transition_log": [
                        {
                            "when": t.when,
                            "state": t.state,
                            "event": t.event,
                            "down_reason": t.down_reason
                        }
                        for t in entry.transition_log
                    ]
                }
                for entry in self.entries
            ]
        }


# ========================================
# show route summary | no-more
# ========================================
@dataclass
class ShowRouteSummaryHighwater:
    """Represents highwater mark statistics"""
    rib_unique_destination_routes: str = ""
    rib_routes: str = ""
    fib_routes: str = ""
    vrf_type_routing_instances: str = ""

@dataclass
class ShowRouteSummaryProtocol:
    """Represents protocol statistics for a routing table"""
    protocol: str
    routes: int
    active: int

@dataclass
class ShowRouteSummaryTable:
    """Represents a routing table summary"""
    table_name: str
    destinations: int
    routes: int
    active: int
    holddown: int
    hidden: int
    protocols: List[ShowRouteSummaryProtocol] = field(default_factory=list)

@dataclass
class ShowRouteSummary:
    """Represents the complete route summary output"""
    autonomous_system: str = ""
    router_id: str = ""
    highwater: Optional[ShowRouteSummaryHighwater] = None
    tables: List[ShowRouteSummaryTable] = field(default_factory=list)
    
    def to_dict(self):
        """Convert to dictionary format"""
        result = {
            "autonomous_system": self.autonomous_system,
            "router_id": self.router_id,
            "tables": [
                {
                    "table_name": table.table_name,
                    "destinations": table.destinations,
                    "routes": table.routes,
                    "active": table.active,
                    "holddown": table.holddown,
                    "hidden": table.hidden,
                    "protocols": [
                        {
                            "protocol": proto.protocol,
                            "routes": proto.routes,
                            "active": proto.active
                        }
                        for proto in table.protocols
                    ]
                }
                for table in self.tables
            ]
        }
        
        if self.highwater:
            result["highwater"] = {
                "rib_unique_destination_routes": self.highwater.rib_unique_destination_routes,
                "rib_routes": self.highwater.rib_routes,
                "fib_routes": self.highwater.fib_routes,
                "vrf_type_routing_instances": self.highwater.vrf_type_routing_instances
            }
        
        return result


# ========================================
# Commands 17-22: No new models required
# ========================================
# Command 17 (show rsvp session match dn) - Uses ShowRsvpSession (empty)
# Command 18 (show mpls lsp unidirectional match dn) - Uses ShowMplsLsp (empty)
# Command 19 (show rsvp session first) - Uses ShowRsvpSession
# Command 20 (show rsvp session second) - Uses ShowRsvpSession
# Command 21 (show rsvp session ma) - Uses ShowRsvpSession (empty)
# Command 22 (show mpls lsp unidirectional) - Uses ShowMplsLsp