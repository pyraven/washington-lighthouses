import os
import json
import re
import folium


def parse_coordinates(lighthouse_coords):
	pattern = re.search("(\d+.\d+).*?(\d+.\d+)", lighthouse_coords)
	if pattern:
		latitude = float(pattern.group(1))
		longtitude = float(pattern.group(2))
		neg_longtitude = float("-" + str(longtitude).replace('\U00002013', '-'))
		return [latitude, neg_longtitude]
	else:
		return None


def build_map():
	lighthouse_data = os.path.join("lighthouse_data.json")
	jsonfile = open(lighthouse_data, 'r')
	data = json.loads(jsonfile.read())
	lighthouse_count = 0
	point_one = parse_coordinates((data[0]["Coordinates"]))
	m = folium.Map(location=point_one, zoom_start=7)
	for points in data:
		lighthouse_dic = {
			"Name": points["Name"],
			"Location": points["Location"],
			"Current Lens": points["Current Lens"],
			"Year first lit": points["Year first lit"],
			"Focal Height": points["Focal Height"],
			"Automated": points["Automated"],
			"Coordinates": parse_coordinates(points["Coordinates"]),
			"Year deactivated": points["Year deactivated"]
		}
		if points["Coordinates"] is not None:
			if points["Name"] != "Skunk Bay Light":
				if points["Year deactivated"] == "Active":
					active_map_tip = "Active. Click here for more info!"
					folium.Marker(lighthouse_dic["Coordinates"],
					popup='<strong>' + '\n' +
						  f'{lighthouse_dic["Name"]}\n' +
						  f'Location: {lighthouse_dic["Location"]}\n'
						  f'Current Lens: {lighthouse_dic["Current Lens"]}\n'	
						  'Location</strong>',
					tooltip=active_map_tip).add_to(m)
					lighthouse_count +=1
				else:
					inactive_map_tip = "Inactive"
					folium.Marker(lighthouse_dic["Coordinates"],
					popup='<strong>Location</strong>',
					tooltip=inactive_map_tip).add_to(m)
					lighthouse_count +=1
			else:
				# Using coordinates based on this url
				# to map Skunk Bay Lighthouse since its missing
				# from wikipedia page
				# http://lighthousefriends.com/light.asp?ID=111
				sbl_coords = [47.91925, -122.56981]
				sbl_map_tip = "Active. Click here for more info!"
				folium.Marker(sbl_coords,
				popup='<strong>Location</strong>',
				tooltip=sbl_map_tip).add_to(m)
				lighthouse_count +=1
	m.save("washington-lighthouses.html")
	print(f"Active Lighthouses plotted: {lighthouse_count}")


if __name__ == "__main__":
	build_map()