import pandas as pd


def generate_car_matrix(dataset_path):

    df = pd.read_csv(dataset_path)


    car_matrix = df.pivot_table(index='id_1', columns='id_2', values='car', fill_value=0)

    car_matrix.values[[range(len(car_matrix))]*2] = 0

    return car_matrix

dataset_path = 'dataset-1.csv'
result_matrix = generate_car_matrix(dataset_path)
print(result_matrix)


def get_type_count(df):

    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    type_count = df['car_type'].value_counts().to_dict()

  
    type_count = dict(sorted(type_count.items()))

    return type_count


dataset_path = 'dataset-1.csv'
df = pd.read_csv(dataset_path)
result = get_type_count(df)
print(result)

def get_bus_indexes(df):

    mean_bus_value = df['bus'].mean()


    bus_indexes = df[df['bus'] > 2 * mean_bus_value].index.tolist()


    bus_indexes.sort()

    return bus_indexes


dataset_path = 'dataset-1.csv'
df = pd.read_csv(dataset_path)
result = get_bus_indexes(df)
print(result)

def filter_routes(df):
  
    route_avg_truck = df.groupby('route')['truck'].mean()


    selected_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

  
    selected_routes.sort()

    return selected_routes


dataset_path = 'dataset-1.csv'
df = pd.read_csv(dataset_path)
result = filter_routes(df)
print(result)


def multiply_matrix(car_matrix):
    
    modified_matrix = car_matrix.copy()

  
    modified_matrix[modified_matrix > 20] *= 0.75
    modified_matrix[modified_matrix <= 20] *= 1.25

    
    modified_matrix = modified_matrix.round(1)

    return modified_matrix

result_matrix = generate_car_matrix('dataset-1.csv')
modified_result = multiply_matrix(result_matrix)
print(modified_result)


def check_time_completeness(df):
  
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])

    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    twenty_four_hours = pd.to_timedelta('1 day')

    incorrect_timestamps = df.groupby(['id', 'id_2']).apply(lambda group: (
        (group['start_timestamp'].min() != pd.Timestamp('00:00:00')) |
        (group['end_timestamp'].max() != pd.Timestamp('23:59:59')) |
        (group['start_timestamp'].max() - group['end_timestamp'].min() > twenty_four_hours) |
        (group['start_timestamp'].dt.dayofweek.nunique() != 7)
    )).any(level=['id', 'id_2'])

    return incorrect_timestamps

df = pd.read_csv('dataset-2.csv')
result = check_time_completeness(df)
print(result)
