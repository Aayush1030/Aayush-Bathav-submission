import pandas as pd
import networkx as nx

def calculate_distance_matrix(dataset_path):
    
    df = pd.read_csv(dataset_path)

    G = nx.from_pandas_edgelist(df, 'start_id', 'end_id', ['distance'], create_using=nx.DiGraph())

    distance_matrix = nx.floyd_warshall_numpy(G, weight='distance')

    distance_matrix[distance_matrix == float('inf')] = 0


    distance_df = pd.DataFrame(distance_matrix, index=df['start_id'].unique(), columns=df['start_id'].unique())

    return distance_df

dataset_path = 'dataset-3.csv'
result_distance_matrix = calculate_distance_matrix(dataset_path)
print(result_distance_matrix)

def unroll_distance_matrix(distance_matrix):
    unrolled_data = []

    for id_start in distance_matrix.index:
        
        for id_end in distance_matrix.columns:
          
            if id_start != id_end:
                
                unrolled_data.append({
                    'id_start': id_start,
                    'id_end': id_end,
                    'distance': distance_matrix.loc[id_start, id_end]
                })

    
    unrolled_df = pd.DataFrame(unrolled_data)

    return unrolled_df

result_unrolled_df = unroll_distance_matrix(result_distance_matrix)
print(result_unrolled_df)


def find_ids_within_ten_percentage_threshold(unrolled_distance_df, reference_id_start):
   
    reference_rows = unrolled_distance_df[unrolled_distance_df['id_start'] == reference_id_start]

    reference_avg_distance = reference_rows['distance'].mean()

    
    threshold = 0.1 * reference_avg_distance

    ids_within_threshold = reference_rows[
        (reference_rows['distance'] >= (reference_avg_distance - threshold)) &
        (reference_rows['distance'] <= (reference_avg_distance + threshold))
    ]['id_start'].unique()

   
    ids_within_threshold.sort()

    return ids_within_threshold


reference_id = 123  
result_ids_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled_df, reference_id)
print(result_ids_within_threshold)


def calculate_toll_rate(unrolled_distance_df):
    
    unrolled_distance_df['moto'] = 0.8 * unrolled_distance_df['distance']
    unrolled_distance_df['car'] = 1.2 * unrolled_distance_df['distance']
    unrolled_distance_df['rv'] = 1.5 * unrolled_distance_df['distance']
    unrolled_distance_df['bus'] = 2.2 * unrolled_distance_df['distance']
    unrolled_distance_df['truck'] = 3.6 * unrolled_distance_df['distance']

    return unrolled_distance_df

result_with_toll_rates = calculate_toll_rate(result_unrolled_df)
print(result_with_toll_rates)


def calculate_time_based_toll_rates(df):

    df_with_time_rates = df.copy()

    
    weekdays_morning_range = pd.to_datetime(['00:00:00', '10:00:00']).time
    weekdays_afternoon_range = pd.to_datetime(['10:00:00', '18:00:00']).time
    weekdays_evening_range = pd.to_datetime(['18:00:00', '23:59:59']).time

    
    df_with_time_rates['start_time'] = pd.to_datetime(df_with_time_rates['start_time'])
    df_with_time_rates['end_time'] = pd.to_datetime(df_with_time_rates['end_time'])

   
    def calculate_discount_factor(row):
        if row['start_time'].weekday() < 5:  
            if weekdays_morning_range[0] <= row['start_time'].time() <= weekdays_morning_range[1]:
                return 0.8
            elif weekdays_afternoon_range[0] <= row['start_time'].time() <= weekdays_afternoon_range[1]:
                return 1.2
            elif weekdays_evening_range[0] <= row['start_time'].time() <= weekdays_evening_range[1]:
                return 0.8
        else: 
            return 0.7

  
    df_with_time_rates['discount_factor'] = df_with_time_rates.apply(calculate_discount_factor, axis=1)

    
    vehicle_columns = ['moto', 'car', 'rv', 'bus', 'truck']
    for column in vehicle_columns:
        df_with_time_rates[column] *= df_with_time_rates['discount_factor']

  
    df_with_time_rates['start_day'] = df_with_time_rates['start_time'].dt.day_name()
    df_with_time_rates['end_day'] = df_with_time_rates['end_time'].dt.day_name()

    df_with_time_rates = df_with_time_rates.drop(columns=['discount_factor'])

    return df_with_time_rates

result_with_time_rates = calculate_time_based_toll_rates(result_with_toll_rates)
print(result_with_time_rates)
