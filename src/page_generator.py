import os
from inline_markdown import markdown_to_html_node, extract_title

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read template file
    with open(template_path, 'r') as f:
        template_content = f.read()
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    print(f"HTML Node: {html_node}")  # Debug print
    
    if html_node is None:
        print("Error: markdown_to_html_node returned None")
        return

    try:
        html_content = html_node.to_html()
    except Exception as e:
        print(f"Error generating HTML content: {e}")
        return
    
    # Extract title
    try:
        title = extract_title(markdown_content)
    except ValueError:
        title = "Untitled"  # Fallback title if no h1 is found
    
    # Replace placeholders in template
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the full HTML to the destination file
    with open(dest_path, 'w') as f:
        f.write(full_html)

    print(f"Page generated successfully: {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for root, _, files in os.walk(dir_path_content):
        for file in files:
            if file.endswith('.md'):
                # Construct the full path for the markdown file
                md_path = os.path.join(root, file)
                
                # Construct the destination path
                rel_path = os.path.relpath(md_path, dir_path_content)
                dest_path = os.path.join(dest_dir_path, rel_path[:-3] + '.html')
                
                # Ensure the destination directory exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Generate the page
                generate_page(md_path, template_path, dest_path)
                print(f"Generated page: {dest_path}")


                