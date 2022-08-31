import math
import sys
from pykml import parser
from pykml.factory import nsmap

filename = 'C:\ConvertKML\survey.kml'

namespace = {"ns": nsmap[None]}

def deg_to_dms(deg, pretty_print=None, ndp=2):
    """Convert from decimal degrees to degrees, minutes, seconds."""
    m, s = divmod(abs(deg)*3600, 60)
    d, m = divmod(m, 60)
    if deg < 0:
        d = -d
    d, m = int(d), int(m)
    if pretty_print:
        if pretty_print=='latitude':
            hemi = 'N' if d>=0 else 'S'
        elif pretty_print=='longitude':
            hemi = 'E' if d>=0 else 'W'
        else:
            hemi = '?'
        return '{d:d}{m:d}{s:.{ndp:d}f}{hemi:1s}'.format(
                    d=abs(d), m=m, s=s, hemi=hemi, ndp=ndp)
    return d, m, s

def remove_dec(deg, type):
    len_check = str(deg).split(".")
    if (type=="lat"):
        if (len(len_check[0])==6):
            deg = str(deg).replace(".", "0")
        else:
            deg = str(deg).replace(".", "")   
    elif (type=="long"):
        if (len(len_check[0])<6):
            deg = str(deg).replace(".", "0")
        else:
            deg = str(deg).replace(".", "")         
    else:
        deg = str(deg).replace(".", "")
    return deg

def lat_long(lat, long):
    lat = remove_dec(lat, "null")
    long = remove_dec(long, "null")
    combined_lat_long = long[:7] + " " + lat[:7]
    return combined_lat_long    

count = 0
line = 100
with open('C:\ConvertKML\data.txt', 'w') as o:
 with open(filename) as f:
  root = parser.parse(f).getroot()
  pms = root.findall(".//ns:Point", namespaces=namespace)
  print(pms)
  for pm in pms:
    count = count + 1
    results = str(pm.coordinates).split(",")
    formatting ="                    "
    #print(results[0])
    #print(results[1])
    output = (formatting + str(line)+(str(count).rjust(2, '0' )) + " " + remove_dec(deg_to_dms(float(results[1]), pretty_print="latitude"),"long")+remove_dec(deg_to_dms(float(results[0]), pretty_print="longitude"),"lat") + " " + lat_long(results[1], results[0]) + "\n")
    o.writelines(output)
    print(formatting + str(line)+(str(count).rjust(2, '0' )), remove_dec(deg_to_dms(float(results[1]), pretty_print="latitude"),"long")+remove_dec(deg_to_dms(float(results[0]), pretty_print="longitude"),"lat"), lat_long(results[1], results[0]))





