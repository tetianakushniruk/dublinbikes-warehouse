select
    station_id,
    station_name,
    latitude,
    longitude,
    capacity
from {{ ref('stg_station_information') }}