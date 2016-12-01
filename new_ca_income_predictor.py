import httplib2

ADULT_DATA_SET_URL = "http://mf2.dit.ie/machine-learning-income.data"
# TODO: over and under bool... reintroduce...
# TODO: May not need this... fold into calculate_average()... maybe? Or not needed at all... words useless?
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
    # TODO: add comment
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


def attribute_value_counter(record, attr_value_count_dict):
    # TODO: add comment
    for key in attr_value_count_dict.keys():
        if record[key] in attr_value_count_dict[key]:
            attr_value_count_dict[key][record[key]] += 1
        else:
            attr_value_count_dict[key][record[key]] = 1


def divide_values(attr_value_count_dict, record_count):
    # TODO: add comment
    for key in attr_value_count_dict.keys():
        for value in attr_value_count_dict[key]:
            attr_value_count_dict[key][value] /= record_count


def substitute_discrete_values(data_set_list):
    # TODO: add comment
    attr_over50_count_dict = {1: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}}
    attr_under50_count_dict = {1: {}, 5: {}, 6: {}, 7: {}, 8: {}, 9: {}}
    over50_count = 0
    under50_count = 0

    for record in data_set_list:
        if record[-1] == '<=50k':
            attribute_value_counter(record, attr_under50_count_dict)
            under50_count += 1
        else:
            attribute_value_counter(record, attr_over50_count_dict)
            over50_count += 1

    divide_values(attr_over50_count_dict, over50_count)
    divide_values(attr_under50_count_dict, under50_count)

    for record in data_set_list:
        if record[-1] == '<=50k':
            for key in attr_under50_count_dict.keys():
                record[key] = attr_under50_count_dict[key][record[key]]
        else:
            for key in attr_over50_count_dict.keys():
                record[key] = attr_over50_count_dict[key][record[key]]

    return data_set_list


def create_training_testing_data_sets(input_data_set_list, percentage_int=75):
    # TODO: add comment
    requested_records_int = len(input_data_set_list) // 100 * percentage_int

    count = 0

    over_50_training_list = []
    under_50_training_list = []
    testing_list = []

    for record in input_data_set_list:
        if count >= requested_records_int:
            testing_list.append(record)
        elif record[-1] == '<=50k':
            under_50_training_list.append(record)
            count += 1
        else:
            over_50_training_list.append(record)
            count += 1

    return over_50_training_list, under_50_training_list, testing_list


def calculate_average(data_set_list):
    # TODO: add comment
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
    # TODO: add comment
    test_values_dict = {}

    for key in data_set_one_dict.keys():
        test_values_dict[key] = ((data_set_one_dict[key] + data_set_two_dict[key]) / 2)

    return test_values_dict


def income_predictor(test_data_set_list, test_values_dict):
    # TODO: add comment
    correct_predictions_int = 0
    total_records_int = len(test_data_set_list)
    result_str = ''

    for record in test_data_set_list:

        over_50_score_int = 0
        under_50_score_int = 0
        index_count = 0

        for index in MEASURED_INDEXES:
            if record[index] > test_values_dict[KEYS_TUPLE[index_count]]:
                over_50_score_int += 1
            else:
                under_50_score_int += 1
            index_count += 1

        if over_50_score_int >= under_50_score_int:
            result_str = '>50k'
        elif over_50_score_int < under_50_score_int:
            result_str = '<=50k'

        if result_str == record[-1]:
            correct_predictions_int += 1

    correct_percentage = 100 * correct_predictions_int // total_records_int

    return correct_percentage, correct_predictions_int, total_records_int


def main():

    data_set_source_list = obtain_data_set(ADULT_DATA_SET_URL)
    sub_data_set_list = substitute_discrete_values(data_set_source_list)

    over50_training_list, under50_training_list, testing_list = create_training_testing_data_sets(sub_data_set_list)

    over50_average_dict = calculate_average(over50_training_list)
    under50_average_dict = calculate_average(under50_training_list)

    testing_values_dict = create_test_values(over50_average_dict, under50_average_dict)

    a,b,c = income_predictor(testing_list, testing_values_dict)

    # TODO: nicer result output
    print(a,b,c)

if __name__ == "__main__":
    main()
