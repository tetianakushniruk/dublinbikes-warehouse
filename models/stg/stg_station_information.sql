with source as (
    select * from {{ source('dublinbikes', 'station_information') }}
)
select
    station_id,
    name            as station_name,
    capacity,
    lat             as latitude,
    lon             as longitude
from source