import re

def analisar_mensagem(msg):
    padrao = r'ID:(\d+);LAT:([-.\d]+);LON:([-.\d]+);SPD:(\d+);EVT:(\w+)'
    match = re.match(padrao, msg)

    if match:
        return {
            "id": match.group(1),
            "latitude": float(match.group(2)),
            "longitude": float(match.group(3)),
            "velocidade": int(match.group(4)),
            "evento": match.group(5),
            "valido": True
        }
    else:
        return {"mensagem": msg, "valido": False}
