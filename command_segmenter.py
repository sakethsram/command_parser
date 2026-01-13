import re

def read_mx80_show_commands(file_path):
    """
    Reads all Juniper MX80 show command output from a text file
    and returns it as a single string.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        mx80_show_commands_output = f.read()

    return mx80_show_commands_output

def extract_show_arp_output_1(terminal_output: str):
    """
    Extracts the output of:
    'show arp no-resolve | no-more'

    Starts at the command line and ends at:
    'Total entries: <number>'
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+arp\s+no-resolve\s*\|\s*no-more"
        r"(.*?)"
        r"Total\s+entries:\s*\d+"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE)

    if match:
        # Get the full matched text
        full_match = match.group(0).strip()
        
        # Remove the command line and keep only the table + "Total entries" line
        lines = full_match.split('\n')
        if lines:
            # Skip the first line (command) and join the rest
            return '\n'.join(lines[1:]).strip()
    
    return None


def extract_show_vrrp_summary_output_2(terminal_output: str):
    """
    Extracts the output of:
    'show vrrp summary | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+vrrp\s+summary\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_lldp_neighbors_output_3(terminal_output: str):
    """
    Extracts the output of:
    'show lldp neighbors | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+lldp\s+neighbors\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_bfd_session_output_4(terminal_output: str):
    """
    Extracts the output of:
    'show bfd session | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+bfd\s+session\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_rsvp_neighbor_output_5(terminal_output: str):
    """
    Extracts the output of:
    'show rsvp neighbor | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+rsvp\s+neighbor\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_rsvp_session_output_6(terminal_output: str):
    """
    Extracts the output of:
    'show rsvp session | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+rsvp\s+session\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_route_table_inet0_output_7(terminal_output: str):
    """
    Extracts the output of:
    'show route table inet.0 | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+route\s+table\s+inet\.0\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_route_table_inet3_output_8(terminal_output: str):
    """
    Extracts the output of:
    'show route table inet.3 | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+route\s+table\s+inet\.3\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_route_table_mpls0_output_9(terminal_output: str):
    """
    Extracts the output of:
    'show route table mpls.0 | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+route\s+table\s+mpls\.0\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_mpls_interface_output_10(terminal_output: str):
    """
    Extracts the output of:
    'show mpls interface | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+mpls\s+interface\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_mpls_lsp_output_11(terminal_output: str):
    """
    Extracts the output of:
    'show mpls lsp | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+mpls\s+lsp\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_mpls_lsp_p2mp_output_12(terminal_output: str):
    """
    Extracts the output of:
    'show mpls lsp p2mp | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+mpls\s+lsp\s+p2mp\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_bgp_summary_output_13(terminal_output: str):
    """
    Extracts the output of:
    'show bgp summary | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+bgp\s+summary\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_bgp_neighbor_output_14(terminal_output: str):
    """
    Extracts the output of:
    'show bgp neighbor | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+bgp\s+neighbor\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_isis_adjacency_extensive_output_15(terminal_output: str):
    """
    Extracts the output of:
    'show isis adjacency extensive | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+isis\s+adjacency\s+extensive\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_route_summary_output_16(terminal_output: str):
    """
    Extracts the output of:
    'show route summary | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+route\s+summary\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_rsvp_session_match_dn_output_17(terminal_output: str):
    """
    Extracts the output of:
    'show rsvp session | match DN |no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+rsvp\s+session\s*\|\s*match\s+DN\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_mpls_lsp_unidirectional_match_dn_output_18(terminal_output: str):
    """
    Extracts the output of:
    'show mpls lsp unidirectional | match Dn |no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+mpls\s+lsp\s+unidirectional\s*\|\s*match\s+Dn\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_rsvp_session_first_output_19(terminal_output: str):
    """
    Extracts the FIRST occurrence of:
    'show rsvp session'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+rsvp\s+session\s*$"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_rsvp_session_second_output_20(terminal_output: str):
    """
    Extracts the SECOND occurrence of:
    'show rsvp session'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = r"show\s+rsvp\s+session\s*$"
    
    matches = []
    for match in re.finditer(pattern, terminal_output, re.MULTILINE | re.IGNORECASE):
        start_pos = match.start()
        # Find the end (next prompt or end of string)
        next_prompt_pattern = r"^\S+@\S+>"
        next_match = re.search(next_prompt_pattern, terminal_output[match.end():], re.MULTILINE)
        
        if next_match:
            end_pos = match.end() + next_match.start()
        else:
            end_pos = len(terminal_output)
        
        output = terminal_output[start_pos:end_pos].strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            matches.append('\n'.join(lines[1:]).strip())
        else:
            matches.append(None)
    
    # Return the second occurrence if it exists
    if len(matches) >= 2:
        return matches[1]
    
    return None


def extract_show_rsvp_session_ma_output_21(terminal_output: str):
    """
    Extracts the output of:
    'show rsvp session    | ma      no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+rsvp\s+session\s+\|\s+ma\s+no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


def extract_show_mpls_lsp_unidirectional_output_22(terminal_output: str):
    """
    Extracts the output of:
    'show mpls lsp unidirectional | no-more'

    Starts at the command line.
    Ends right before the next prompt.
    Returns the output without the command line.
    """
    pattern = (
        r"show\s+mpls\s+lsp\s+unidirectional\s*\|\s*no-more"
        r"(.*?)"
        r"(?=^\S+@\S+>|\Z)"
    )

    match = re.search(pattern, terminal_output, re.DOTALL | re.IGNORECASE | re.MULTILINE)

    if match:
        output = match.group(0).strip()
        output = output.rsplit("\n", 1)[0]
        # Remove the first line (command)
        lines = output.split('\n')
        if len(lines) > 1:
            return '\n'.join(lines[1:]).strip()
        return None

    return None


if __name__ == "__main__":

    s = read_mx80_show_commands(file_path="pre_check.txt")
    print("extract_show_arp_output_1:")
    print(extract_show_arp_output_1(s))
    
    # print("\nextract_show_vrrp_summary_output_2:")
    # print(extract_show_vrrp_summary_output_2(s))
    
    # print("\nextract_show_lldp_neighbors_output_3:")
    # print(extract_show_lldp_neighbors_output_3(s))
    
    # print("\nextract_show_bfd_session_output_4:")
    # print(extract_show_bfd_session_output_4(s))
    
    # print("\nextract_show_rsvp_neighbor_output_5:")
    # print(extract_show_rsvp_neighbor_output_5(s))
    
    # print("\nextract_show_rsvp_session_output_6:")
    # print(extract_show_rsvp_session_output_6(s))
    
    # print("\nextract_show_route_table_inet0_output_7:")
    # print(extract_show_route_table_inet0_output_7(s))
    
    # print("\nextract_show_route_table_inet3_output_8:")
    # print(extract_show_route_table_inet3_output_8(s))
    
    # print("\nextract_show_route_table_mpls0_output_9:")
    # print(extract_show_route_table_mpls0_output_9(s))
    
    # print("\nextract_show_mpls_interface_output_10:")
    # print(extract_show_mpls_interface_output_10(s))
    
    # print("\nextract_show_mpls_lsp_output_11:")
    # print(extract_show_mpls_lsp_output_11(s))
    
    # print("\nextract_show_mpls_lsp_p2mp_output_12:")
    # print(extract_show_mpls_lsp_p2mp_output_12(s))
    
    # print("\nextract_show_bgp_summary_output_13:")
    # print(extract_show_bgp_summary_output_13(s))
    
    # print("\nextract_show_bgp_neighbor_output_14:")
    # print(extract_show_bgp_neighbor_output_14(s))
    
    # print("\nextract_show_isis_adjacency_extensive_output_15:")
    # print(extract_show_isis_adjacency_extensive_output_15(s))
    
    # print("\nextract_show_route_summary_output_16:")
    # print(extract_show_route_summary_output_16(s))
    
    # print("\nextract_show_rsvp_session_match_dn_output_17:")
    # print(extract_show_rsvp_session_match_dn_output_17(s))
    
    # print("\nextract_show_mpls_lsp_unidirectional_match_dn_output_18:")
    # print(extract_show_mpls_lsp_unidirectional_match_dn_output_18(s))
    
    # print("\nextract_show_rsvp_session_first_output_19:")
    # print(extract_show_rsvp_session_first_output_19(s))
    
    # print("\nextract_show_rsvp_session_second_output_20:")
    # print(extract_show_rsvp_session_second_output_20(s))
    
    # print("\nextract_show_rsvp_session_ma_output_21:")
    # print(extract_show_rsvp_session_ma_output_21(s))
    
    # print("\nextract_show_mpls_lsp_unidirectional_output_22:")
    # print(extract_show_mpls_lsp_unidirectional_output_22(s))