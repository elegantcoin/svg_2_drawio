def convert_xml2draw(filename):
    xml_msg = '<mxGraphModel dx='
    idx_, counter = 2, 0
    polygon_flag = False
    with open('C:\\Users\\XXXXXX\\PycharmProjects\\sgm\\'+filename+'.svg', 'r', encoding='utf-8-sig') as f:
        i = 0
        for line in f:
            i += 1
            if not line.startswith("<"):
                print(line)
            if line.startswith("<svg"):
                data = line.split(" ")
                dx, dy = data[1][6:], data[2][7:]
                print(dx, dy)
                xml_msg += dx+' dy='+dy
                xml_msg += """ grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0"><root>"""
                xml_msg += """\n<mxCell id="0"/>"""
                xml_msg += """\n<mxCell id="1" parent="0"/>"""
            elif line.startswith("<rect"):
                counter += 1
                polygon_flag = False
                rect = line.split("rx=")[0].split("fill")[0].split("<rect")[1]
                # print(rect)
            elif line.startswith("<polygon"):
                counter += 1
                polygon_flag = True
                polygon = line.split(" fill=")[0].split("points=")[1][1:-1]
                polygon_list = [int(s) for s in polygon.split(",")]
                width = 2*(polygon_list[2]-polygon_list[0])
                height = 2*(polygon_list[3]-polygon_list[1])
                x, y = polygon_list[0]-width//2, polygon_list[3]-height//2
                rect = f' x="{x}" y="{y}" width="{width}" height="{height}" '
            elif line.startswith("<text"):
                line = line.replace("->", "|arrow1|")
                line = line.replace(" >", "|arrow2|")
                line = line.replace(" <", "|arrow3|")
                txt = line.split(">")[-2].split("<")[0]
                txt = txt.replace("|arrow1|", "->")
                txt = txt.replace("|arrow2|", ">")
                txt = txt.replace("|arrow3|", "<")
                # txt =line.split("style=")[0].split("<text")[1]
                xml_msg += '\n'+f'<mxCell id="{idx_}" '
                if polygon_flag:
                    xml_msg += f'value="{txt}" style="rhombus;whiteSpace=wrap;html=1;" parent="1" vertex="1"><mxGeometry'
                else:
                    xml_msg += f'value="{txt}" style="strokeWidth=1;" parent="1" vertex="1"><mxGeometry'
                xml_msg += f'{rect}as="geometry"/></mxCell>'
                counter -= 1
                idx_ += 1
                # print(txt)
            elif line.startswith("<polyline"):
                polyline = line.split(" fill=")[0].split("points=")[1][1:-1]
                polypoint = polyline.split(",")
                # print(polypoint)
                single_arrow = False
                if abs(int(polypoint[0])-int(polypoint[2]) == 2) and int(polypoint[3])-int(polypoint[1]) == 6:
                    # down arrow,reverse
                    single_arrow = True
                    polypoint[1],polypoint[-1] = polypoint[-1],polypoint[1]
                elif abs(int(polypoint[0])-int(polypoint[2]) == 2) and int(polypoint[3])-int(polypoint[1]) == -6:
                    # up arrow,reverse
                    single_arrow = True
                    polypoint[1],polypoint[-1] = polypoint[-1],polypoint[1]
                else:
                    pass
                xml_msg += f'\n<mxCell id="{idx_}" value="" style="endArrow=classic;html=1;rounded=0;edgeStyle=orthogonalEdgeStyle;" edge="1" parent="1"><mxGeometry width="50" height="50" relative="1" as="geometry">'
                need = False
                point_tmp = ""
                for i in range(0, len(polypoint), 2):
                    if i == 0:
                        xml_msg += f'<mxPoint x="{polypoint[i]}" y="{polypoint[i+1]}" as="sourcePoint"/>'
                    elif i == len(polypoint)-2:
                        xml_msg += f'<mxPoint x="{polypoint[i]}" y="{polypoint[i+1]}" as="targetPoint"/>'
                    else:
                        need = True
                        point_tmp += f'<mxPoint x="{polypoint[i]}" y="{polypoint[i+1]}"/>'
                if need and (not single_arrow):
                    xml_msg += '<Array as="points">'
                    xml_msg += point_tmp + '</Array>'
                xml_msg += f'</mxGeometry></mxCell>'
                idx_ += 1
            else:
                continue
    xml_msg += '\n</root></mxGraphModel>'

    with open("C:\\Users\\XXXXXX\\PycharmProjects\\sgm\\"+filename+".drawio", "a+") as fw:
        fw.write(xml_msg)

    return xml_msg

if __name__ == "__main__":
    filename = "SpiralReferenceLineSmoother"
    convert_xml2draw(filename)