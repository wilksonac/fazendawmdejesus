import os

# Configuration
directory = r"c:\Users\Admin\OneDrive - NAV Brasil\Documentos\ANTIGRAVITY\fazendawmdejesus"
tailwind_script = '<script src="https://cdn.tailwindcss.com"></script>'
navbar_html = """
    <!-- SHARED NAVBAR START -->
    <nav class="bg-emerald-700 text-white shadow-md sticky top-0 z-50 print:hidden">
        <div class="container mx-auto px-4">
            <div class="flex items-center justify-between h-14">
                <a href="index.html" class="font-bold text-lg flex items-center space-x-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/></svg>
                    <span>WM de Jesus</span>
                </a>
                <div class="flex space-x-1 overflow-x-auto">
                     <a href="index.html" class="px-3 py-2 rounded hover:bg-emerald-600 text-sm whitespace-nowrap transition-colors">Início</a>
                    <a href="leite_colaborativo.html" class="px-3 py-2 rounded hover:bg-emerald-600 text-sm whitespace-nowrap transition-colors">Leite</a>
                    <a href="despesas.html" class="px-3 py-2 rounded hover:bg-emerald-600 text-sm whitespace-nowrap transition-colors">Despesas</a>
                    <a href="financeiro.html" class="px-3 py-2 rounded hover:bg-emerald-600 text-sm whitespace-nowrap transition-colors">Financeiro</a>
                    <a href="registro_animais.html" class="px-3 py-2 rounded hover:bg-emerald-600 text-sm whitespace-nowrap transition-colors">Rebanho</a>
                     <a href="vacas_producao.html" class="px-3 py-2 rounded hover:bg-emerald-600 text-sm whitespace-nowrap transition-colors">Produção</a>
                </div>
            </div>
        </div>
    </nav>
    <!-- SHARED NAVBAR END -->
"""

count = 0

print(f"Scanning directory: {directory}")

for filename in os.listdir(directory):
    if filename.endswith(".html"):
        filepath = os.path.join(directory, filename)
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            original_content = content
            
            # 1. Inject Tailwind if missing
            if "cdn.tailwindcss.com" not in content:
                print(f"Adding Tailwind to {filename}")
                if "</head>" in content:
                    content = content.replace("</head>", f"{tailwind_script}\n</head>")
                else:
                    print(f"WARNING: No </head> tag in {filename}")

            # 2. Inject Navbar (Prevent double injection)
            if "SHARED NAVBAR START" not in content:
                # Basic check for body tag
                if "<body" in content:
                    # Find the end of the opening body tag
                    body_start_index = content.find("<body")
                    body_tag_end_index = content.find(">", body_start_index) + 1
                    
                    if body_tag_end_index > 0:
                        content = content[:body_tag_end_index] + "\n" + navbar_html + content[body_tag_end_index:]
                        print(f"Injected Navbar into {filename}")
                        count += 1
                else:
                     print(f"WARNING: No <body> tag in {filename}")
            else:
                print(f"Navbar already present in {filename}, skipping.")

            # Save if changed
            if content != original_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print(f"Finished. Updated {count} files.")
