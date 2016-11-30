import httplib2

ADULT_DATA_SET_URL = "http://mf2.dit.ie/machine-learning-income.data"


def obtain_data_set(data_set_url):

    http_get = httplib2.Http(".cache")
    header, content = http_get.request(data_set_url)

    downloaded_file_str = content.decode().strip()
    downloaded_file_list = downloaded_file_str.split("\r\n")

    data_set_list = []

    for record in downloaded_file_list:
        try:
            if ' ?' in record:
                raise Exception('Record with invalid values found:', record)
        except Exception:
                continue

        temp_value_list = record.split(',')
        record_value_list = [value.strip().lower() for value in temp_value_list]
        data_set_list.append(record_value_list)

    return data_set_list


def create_training_sets():
    pass


def count_discrete_values(data_set_list):
    attr_value_count_dict = {1: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}}
    record_total_int = len(data_set_list)

    for record in data_set_list:
        for key in attr_value_count_dict.keys():
            if record[key] in attr_value_count_dict[key]:
                attr_value_count_dict[key][record[key]] += 1
            else:
                attr_value_count_dict[key][record[key]] = 1

    for key in attr_value_count_dict.keys():
        for value in attr_value_count_dict[key]:
            attr_value_count_dict[key][value] /= record_total_int

    for record in data_set_list:
        for key in attr_value_count_dict.keys():
            record[key] = attr_value_count_dict[key][record[key]]

    return data_set_list


def main():
    data_set_source_list = obtain_data_set(ADULT_DATA_SET_URL)
    substitute_data_set_list = count_discrete_values(data_set_source_list)

    for record in substitute_data_set_list:
        print(record)

if __name__ == "__main__":
    main()


