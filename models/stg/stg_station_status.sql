with source as (
    select * from {{ source('dublinbikes', 'station_status') }}
)
select
    station_id,
    num_bikes_available as bikes_available,
    num_docks_available as docks_available,
    to_timestamp(last_reported)                       as recorded_at,
    date_trunc('minute', to_timestamp(last_reported)) as recorded_at_minute
from source