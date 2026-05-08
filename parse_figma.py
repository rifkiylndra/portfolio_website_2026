import json

def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(int(r*255), int(g*255), int(b*255))

def process_node(node, level=0):
    indent = "  " * level
    name = node.get("name", "")
    type_ = node.get("type", "")
    
    print(f"{indent}- {name} ({type_})")
    
    # dimensions
    box = node.get("absoluteBoundingBox", {})
    if box:
        print(f"{indent}  width: {box.get('width')}, height: {box.get('height')}")
        
    # corner radius
    if "cornerRadius" in node:
        print(f"{indent}  cornerRadius: {node['cornerRadius']}")
        
    # padding & spacing
    if "paddingLeft" in node:
        print(f"{indent}  padding: {node.get('paddingTop')} {node.get('paddingRight')} {node.get('paddingBottom')} {node.get('paddingLeft')}")
    if "itemSpacing" in node:
        print(f"{indent}  gap: {node.get('itemSpacing')}")
        
    # colors
    fills = node.get("fills", [])
    for f in fills:
        if f.get("type") == "SOLID" and "color" in f:
            c = f["color"]
            hex_color = rgb_to_hex(c.get('r',0), c.get('g',0), c.get('b',0))
            print(f"{indent}  fill: {hex_color} (opacity: {f.get('opacity', c.get('a', 1))})")
            
    # effects (shadows)
    effects = node.get("effects", [])
    for e in effects:
        if e.get("visible", True):
            print(f"{indent}  effect: {e.get('type')} radius: {e.get('radius')} offset: {e.get('offset')}")
            
    # typography
    style = node.get("style", {})
    if style:
        print(f"{indent}  font: {style.get('fontFamily')} {style.get('fontWeight')} {style.get('fontSize')}px, text: '{node.get('characters', '')[:20]}...'")

    for child in node.get("children", []):
        process_node(child, level + 1)

with open("figma_node_utf8.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    nodes = data.get("nodes", {})
    for k, v in nodes.items():
        doc = v.get("document", {})
        if doc:
            process_node(doc)

