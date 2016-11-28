#!/usr/bin/python3

import sys

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
LOCAL_FILE_LOCATION_STR = 'adult.data'


def create_data_sets(file_location, percentage_int=75):
    """ Splits 'adult.data' into training and testing sets.

    Opens local CSV file and splits record lines into a list.
    Takes a percentage of records and splits these into two lists of records based on the income attribute.
    Stores remaining records in a third list.

    :param file_location: location of source data set file.
    :param percentage_int: the percentage of records required for training.
    :return: three lists of records as tuples.
    """
    try:
        local_file = open(file_location, 'r')
    except FileNotFoundError as error:
        print(error)
        sys.exit()

    data_set_tmp_list = [line.strip() for line in local_file]

    data_set_csv_list = [line for line in data_set_tmp_list if line != '']

    requested_records_int = len(data_set_csv_list) // 100 * percentage_int

    higher_income_records_list = []
    lower_income_records_list = []
    test_records_list = []

    record_count = 0

    for record in data_set_csv_list:
        
        try:
            if ' ?' in record:
                raise Exception('Record with invalid values found:', record)
        except Exception:
                continue

        temp_value_list = record.split(',')
        
        record_value_list = [value.strip().lower() for value in temp_value_list]

        if record_count >= requested_records_int:
            test_records_list.append(tuple(record_value_list))
        elif record_value_list[-1] == '>50k':
            higher_income_records_list.append(tuple(record_value_list))
            record_count += 1
        else:
            lower_income_records_list.append(tuple(record_value_list))
            record_count += 1

    return higher_income_records_list, lower_income_records_list, test_records_list


def count_values(data_set_list):
    """ Counts attribute values in a training data set and returns a dictionary of counts.

    For an attribute with an integer value, add to sum of all values for this attribute and assign to dictionary.
    With an attribute with string values, count the occurrences of the value and assign to dictionary.

    :param data_set_list: a list of adult data set tuples.
    :return: dictionary of counts.
    """
    value_counts_dict = {KEYS_TUPLE[0]: 0,
                         KEYS_TUPLE[1]: {},
                         KEYS_TUPLE[2]: 0,
                         KEYS_TUPLE[3]: {},
                         KEYS_TUPLE[4]: {},
                         KEYS_TUPLE[5]: {},
                         KEYS_TUPLE[6]: {},
                         KEYS_TUPLE[7]: {},
                         KEYS_TUPLE[8]: 0,
                         KEYS_TUPLE[9]: 0,
                         KEYS_TUPLE[10]: 0}

    for record_tuple in data_set_list:
        
        index_count = 0

        for index in MEASURED_INDEXES:
            
            if record_tuple[index].isnumeric():
                value_counts_dict[KEYS_TUPLE[index_count]] += int(record_tuple[index])
                index_count += 1
            else:
                if record_tuple[index] in value_counts_dict[KEYS_TUPLE[index_count]]:
                    value_counts_dict[KEYS_TUPLE[index_count]][record_tuple[index]] += 1
                else:
                    value_counts_dict[KEYS_TUPLE[index_count]][record_tuple[index]] = 1
                index_count += 1

    return value_counts_dict


def compare_values(over50_attribute_dict, under50_attribute_dict):
    """ Compares two dictionaries of value counts for a single attribute.

    Checks if the attribute values are in both input dictionaries.
    Adds value if not present and assigns a place holder count to prevent errors during comparison.
    Compares the attribute values to determine indicators of higher income group and adds the attributes to a list.

    :param over50_attribute_dict: attribute value counts for >50k income bracket.
    :param under50_attribute_dict: attribute value counts for <=50k income bracket.
    :return: tuple of attribute values indicating higher income bracket.
    """
    expanded_over50_dict = {}
    expanded_under50_dict = {}

    test_set = {key for key in over50_attribute_dict.keys() for key in under50_attribute_dict.keys()}

    for key in test_set:
        
        if key not in over50_attribute_dict.keys():
            expanded_over50_dict[key] = 0.0
        else:
            expanded_over50_dict[key] = over50_attribute_dict[key]
        if key not in under50_attribute_dict.keys():
            expanded_under50_dict[key] = 0.0
        else:
            expanded_under50_dict[key] = under50_attribute_dict[key]

    higher_attributes_list = [key for key in expanded_over50_dict.keys()
                              if expanded_over50_dict[key] >= expanded_under50_dict[key]]

    return tuple(higher_attributes_list)


def create_test_values(over50_values_dict, under50_values_dict, total_over50_records_int, total_under50_records_int):
    """ Creates a dictionary of values that indicate an income over 50k.

    For each tested attribute with an integer value, the over and under 50k values are averaged
    and added to a test values dictionary.
    For attributes with string values a percentage of the total for the income bracket is calculated.
    The results are used as arguments to call a function that returns a tuple of attribute values
    that occur more often in the higher income bracket. This is then added to the test values dictionary.

    :param over50_values_dict: value counts of >50k income bracket.
    :param under50_values_dict: value counts of <=50k income bracket.
    :param total_over50_records_int: total number of records in the >50k training data set.
    :param total_under50_records_int: total number of records in the <=50k training data set.
    :return: dictionary of values for testing against with income prediction.
    """

    test_values_dict = {}

    for attribute_key in KEYS_TUPLE:
        
        if isinstance(over50_values_dict[attribute_key], int):
            
            over50_float = over50_values_dict[attribute_key] // total_over50_records_int
            under50_float = under50_values_dict[attribute_key] // total_under50_records_int
            under_bool = False
            
            if over50_float >= under50_float:
                average_float = (over50_float + under50_float) / 2
            else:
                average_float = (over50_float + under50_float) / 2
                under_bool = True
            test_values_dict[attribute_key] = (average_float, under_bool)
            
        else:
            
            weighted_attr_one_dict = {}
            weighted_attr_two_dict = {}
            
            for key in over50_values_dict[attribute_key].keys():
                weighted_attr_one_dict[key] = over50_values_dict[attribute_key][key] / total_over50_records_int
                
            for key in under50_values_dict[attribute_key].keys():
                weighted_attr_two_dict[key] = under50_values_dict[attribute_key][key] / total_under50_records_int
                
            test_values_dict[attribute_key] = compare_values(weighted_attr_one_dict, weighted_attr_two_dict)

    return test_values_dict


def income_predictor(test_data_list, test_values_dict):
    """ Compares each record in test data set against training test data values to determine income bracket.

    Integer attribute values are checked to see if they are over the test threshold in the test data values.
    They are then given a score dependant on the result.
    String attribute values are checked to see if they are in the tuple of values for an attribute
    in the test data dictionary and scored accordingly.

    The final scores for a record are compared and a prediction is made. The actual income bracket is compared
    with the prediction and a correct predictions counter is incremented if correct.

    :param test_data_list: list of records as tuples for attempting to predict income bracket.
    :param test_values_dict: dictionary of values to compare against that indicate higher income.
    :return: the percentage that were predicted successfully,
             number of correctly predicted records,
             total number of records in test data set.
    """

    correct_predictions_int = 0
    total_records_int = len(test_data_list)
    result_str = ''

    for record in test_data_list:

        over_50_score_int = 0
        under_50_score_int = 0

        index_count = 0

        for index in MEASURED_INDEXES:
            
            if record[index].isnumeric():
                if float(record[index]) > test_values_dict[KEYS_TUPLE[index_count]][0] \
                        and test_values_dict[KEYS_TUPLE[index_count]][1] is False:
                    over_50_score_int += 1
                elif float(record[index]) < test_values_dict[KEYS_TUPLE[index_count]][0] \
                        and test_values_dict[KEYS_TUPLE[index_count]][1] is True:
                    over_50_score_int += 1
                else:
                    under_50_score_int += 1
            else:
                if record in test_values_dict[KEYS_TUPLE[index_count]]:
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

    over50_list, under50_list, test_records_list = create_data_sets(LOCAL_FILE_LOCATION_STR)

    over50_count_dict = count_values(over50_list)
    under50_count_dict = count_values(under50_list)

    test_values_dict = create_test_values(over50_count_dict, under50_count_dict, len(over50_list), len(under50_list))
    
    correct_percentage, correct_predictions, total_records = income_predictor(test_records_list, test_values_dict)

    print("""
    {0}                    
    |                            |
    | Success rate: {1:n}%          |
    |                            |
    | Correct test records: {2:n} |
    |                            |
    | Total test records: {3:n}   |
    |                            |
    {0}
    """.format("=" * 30, correct_percentage, correct_predictions, total_records))

if __name__ == "__main__":
    main()
