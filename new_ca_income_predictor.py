import httplib2

ADULT_DATA_SET_URL = "http://mf2.dit.ie/machine-learning-income.data"


def obtain_data_set(data_set_url):

    http_get = httplib2.Http(".cache")
    header, content = http_get.request(data_set_url)

    downloaded_file_str = content.decode()

    return downloaded_file_str


def count_discrete_values():
    return {}


def main():
    print(obtain_data_set(ADULT_DATA_SET_URL))

if __name__ == "__main__":
    main()


