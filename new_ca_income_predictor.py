import httplib2

ADULT_DATA_SET_URL = "http://mf2.dit.ie/machine-learning-income.data"
KEYS_TUPLE = ('age',
              'work_class',
              'edu_number',
              'marital_status',
              'occupation',
              'relationship',
              'race',
              'sex',
              'capital_gain',
              'capital_loss',
              'hours_per_week')

MEASURED_INDEXES = (0, 1, 4, 5, 6, 7, 8, 9, 10, 11, 12)


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
        for index, value in enumerate(record_value_list):
            if record_value_list[index].isnumeric():
                record_value_list[index] = float(record_value_list[index])
        data_set_list.append(record_value_list)

    return data_set_list


def create_training_sets(data_set_list):

    over_50_list = []
    under_50_list = []

    for record in data_set_list:
        if record[-1] == '>50k':
            over_50_list.append(record)
        else:
            under_50_list.append(record)

    return over_50_list, under_50_list


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


def calculate_average(data_set_list):

    record_total_int = len(data_set_list)
    attribute_sum_dict = {KEYS_TUPLE[0]: 0.0,
                          KEYS_TUPLE[1]: 0.0,
                          KEYS_TUPLE[2]: 0.0,
                          KEYS_TUPLE[3]: 0.0,
                          KEYS_TUPLE[4]: 0.0,
                          KEYS_TUPLE[5]: 0.0,
                          KEYS_TUPLE[6]: 0.0,
                          KEYS_TUPLE[7]: 0.0,
                          KEYS_TUPLE[8]: 0.0,
                          KEYS_TUPLE[9]: 0.0,
                          KEYS_TUPLE[10]: 0.0}

    for record in data_set_list:
        index_count = 0
        for index in MEASURED_INDEXES:
            attribute_sum_dict[KEYS_TUPLE[index_count]] += record[index]
            index_count += 1

    for key in attribute_sum_dict.keys():
        attribute_sum_dict[key] /= record_total_int

    return attribute_sum_dict


def create_test_values(data_set_one_dict, data_set_two_dict):

    test_values_dict = {}

    for key in data_set_one_dict.keys():
        test_values_dict[key] = ((data_set_one_dict[key] + data_set_two_dict[key]) / 2)

    return test_values_dict



def main():
    data_set_source_list = obtain_data_set(ADULT_DATA_SET_URL)

    over50_list, under50_list = create_training_sets(data_set_source_list)
    over50_sub_dict = count_discrete_values(over50_list)
    under50_sub_dict = count_discrete_values(under50_list)

    over50_average_dict = calculate_average(over50_sub_dict)
    under50_average_dict = calculate_average(under50_sub_dict)

    print(create_test_values(over50_average_dict, under50_average_dict))


if __name__ == "__main__":
    main()
