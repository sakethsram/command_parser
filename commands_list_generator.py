def extract_commands():
    """
    Reads juniper_show_command.txt, extracts commands after 'sumar1@CXAPER02',
    returns them as a list, and writes them to a new file.
    """
    commands = []
    
    try:
        # Read the input file
        with open('juniper_show_command.txt', 'r') as f:
            lines = f.readlines()
        
        # Process each line
        for line in lines:
            # Check if the target string is in the line
            if 'sumar1@CXAPER02' in line:
                # Find the position of the string
                idx = line.find('sumar1@CXAPER02')
                # Get everything after that string and strip whitespace
                command = line[idx + len('sumar1@CXAPER02'):].strip()
                
                # Clean up: remove any leading symbols like $, >, etc.
                command = command.lstrip('$ >')
                command = command.strip()
                
                # Only add non-empty commands to the list
                if command:
                    commands.append(command)
        
        # Write commands to output file
        with open('extracted_commands.txt', 'w') as f:
            for cmd in commands:
                f.write(cmd + '\n')
        
        print(f"Found {len(commands)} command(s)")
        print("Commands written to 'extracted_commands.txt'")
        
        return commands
        
    except FileNotFoundError:
        print("Error: 'juniper_show_command.txt' not found!")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []

# Example usage
if __name__ == "__main__":
    # Extract commands and get the list
    command_list = extract_commands()
    
    # Print the extracted commands
    print("\nExtracted commands:")
    for i, cmd in enumerate(command_list, 1):
        print(f"{i}. {cmd}")