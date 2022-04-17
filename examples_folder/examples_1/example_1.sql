CREATE TABLE  test_table_1 AS
select
     sql_views.id
     , sql_views.name
     , sql_views.sql
     , 'view' as tpe
from
    periscope_usage_data.sql_views, periscope_usage_data.sql_views3, periscope_usage_data.sql_views4
join
    periscope_usage_data.sql_views1
join
    periscope_usage_data.sql_views2
where
     sql_views.deleted_at is null