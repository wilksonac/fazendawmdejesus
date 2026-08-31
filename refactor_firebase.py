import os
import re

directory = r"c:\Users\Admin\OneDrive - NAV Brasil\Documentos\ANTIGRAVITY\fazendawmdejesus"
config_file_name = "firebase-config.js"
script_tag = f'<script src="{config_file_name}"></script>'

# Regex to find the config object
# Matches: const firebaseConfig = { ... };
regex_config = re.compile(r'const\s+firebaseConfig\s*=\s*\{[\s\S]*?\};', re.MULTILINE)

count = 0

print(f"Scanning directory: {directory}")

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            original_content = content
            
            # Check if file has firebaseConfig
            if regex_config.search(content):
                print(f"Refactoring {filename}...")
                
                # 1. Inject <script src='firebase-config.js'></script>
                # Prefer putting it before the first script that uses it, or in head.
                # Safe bet: Put it right before the </head> or body.
                # Actually, let's put it right after the SHARED NAVBAR or Tailwind, to be available early.
                # Based on previous step, we have <script src="https://cdn.tailwindcss.com"></script>
                
                if script_tag not in content:
                    if "</head>" in content:
                        content = content.replace("</head>", f"    {script_tag}\n</head>")
                    else:
                        print(f"WARNING: No </head> tag in {filename}")

                # 2. Replace the object definition
                # We replace 'const firebaseConfig = { ... };' with 'const firebaseConfig = window.globalFirebaseConfig;'
                content = regex_config.sub('const firebaseConfig = window.globalFirebaseConfig;', content)
                
                count += 1
            
            # Save if changed
            if content != original_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print(f"Finished. Refactored {count} files.")
