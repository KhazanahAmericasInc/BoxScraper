from gmplot import gmplot

def parseLocationFN(file_name):
    img_data = {}

    data_string = file_name[file_name.index('(') + 1:file_name.index(')')]
    file_type_index = len(data_string) - data_string[::-1].index('.') - 1
    img_data['file_type'] = data_string[file_type_index:]
    data_array = data_string[:file_type_index].split(' ')

    location_data = []
    location_data.append(data_array[6][0:9])
    location_data.append(data_array[6][9:19])

    img_data['weekday'] = data_array[0]
    img_data['month'] = data_array[1]
    img_data['day'] = data_array[2]
    img_data['time'] = data_array[3]
    img_data['time_zone'] = data_array[4]
    img_data['year'] = data_array[5][0:4]
    img_data['zone'] = data_array[5][8]
    img_data['latitude'] = location_data[0]
    img_data['longitude'] = location_data[1]

    img_data['has_location'] = True

    return img_data


def parseNoLocationFN(file_name):
    img_data = {}
    data_string = file_name[file_name.index('(') + 1:file_name.index(')')]
    img_data['file_type'] = data_string[data_string.index('.'):]
    data_array = data_string[:data_string.index('.')].split(' ')

    img_data['weekday'] = data_array[0]
    img_data['month'] = data_array[1]
    img_data['day'] = data_array[2]
    img_data['time'] = data_array[3]
    img_data['time_zone'] = data_array[4]
    img_data['year'] = data_array[5][0:4]
    img_data['zone'] = data_array[5][::-1][0]

    img_data['has_location'] = False

    return img_data

def parseLine(line):
    data_split = line.split(',')
    data_object = {}

    file_name = ''
    img_data = {}

    if 'Location' in  line:
        file_name = data_split[0] + data_split[1]
        data_object['guess_class'] = data_split[2]
        data_object['confidence'] = data_split[3]
        data_object['final_class'] = data_split[4]
        img_data = parseLocationFN(file_name)
    else:
        file_name = data_split[0]
        data_object['guess_class'] = data_split[1]
        data_object['confidence'] = data_split[2]
        data_object['final_class'] = data_split[3] 
        img_data = parseNoLocationFN(file_name)

    data_object['img_data'] = img_data
    return data_object

def main():
    # Place map
    gmap = gmplot.GoogleMapPlotter(37.766956, -122.438481, 12)

    # Get line data
    lines = [line.rstrip('\n') for line in open('net_output.txt')][1:]

    json_data = []
    for line in lines:
        json_data.append(parseLine(line))

    plot_list = []

    for entry in json_data:
        img_data = entry['img_data']
        if img_data['has_location']:
            plots = (float(img_data['latitude']), float(img_data['longitude']))
            plot_list.append(plots)
            #print(img_data['latitude'],img_data['longitude'])

    plot_lats, plot_long = zip(*plot_list)

    gmap.scatter(plot_lats, plot_long , '#3B0B39', size=40, marker=False)

    gmap.draw('my_map.html')

if __name__ == "__main__":
    main()

