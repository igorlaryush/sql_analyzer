from sql_analyzer.functions import analyze, find_parents_names, find_table_names_from_sql

test_files_dir = 'examples_folder/'


def test_analyze_example_1():
    dir_name = test_files_dir + 'examples_1/'
    assert analyze(dir_name).graph == {'periscope_usage_data.sql_views': [],
                                       'periscope_usage_data.sql_views1': [],
                                       'periscope_usage_data.sql_views2': [],
                                       'periscope_usage_data.sql_views3': [],
                                       'periscope_usage_data.sql_views4': [],
                                       'test_table_1': ['periscope_usage_data.sql_views',
                                                        'periscope_usage_data.sql_views1',
                                                        'periscope_usage_data.sql_views2',
                                                        'periscope_usage_data.sql_views3',
                                                        'periscope_usage_data.sql_views4']}


def test_analyze_example_2():
    dir_name = test_files_dir + 'examples_2/'
    assert analyze(dir_name).graph == {'test.test_a': [],
                                       'test.test_a1': [],
                                       'test.test_c': [],
                                       'test.test_d': [],
                                       'test_2': ['test.test_a',
                                                  'test.test_a1',
                                                  'test.test_c',
                                                  'test.test_d',
                                                  'test_table_1'],
                                       'test_table_1': []}


def test_analyze_example_3():
    dir_name = test_files_dir + 'examples_3/'
    assert analyze(dir_name).graph == {'example_3': ['periscope_usage_data.charts',
                                                     'periscope_usage_data.csv',
                                                     'periscope_usage_data.dashboards',
                                                     'periscope_usage_data.sql_views'],
                                       'periscope_usage_data.charts': [],
                                       'periscope_usage_data.csv': [],
                                       'periscope_usage_data.dashboards': [],
                                       'periscope_usage_data.sql_views': []}


def test_find_parents_names_example_1():
    assert find_parents_names('create table test1 as se'.split()) == []


def test_find_parents_names_example_2():
    assert find_parents_names('create table test1 as select * from test2, test3,'.split()) == 'test2 test3'.split()


def test_find_parents_names_example_3():
    assert find_parents_names("""select *
from (
  select col1 from test.test_a join test.test_a1 on a.col1 = a1.col1) a
left join test_table_1 b # comment""".split()) == ['test.test_a', 'test.test_a1', 'test_table_1']


def test_find_table_names_from_sql_file_example_1():
    filename = 'example_1.sql'
    path = test_files_dir + 'examples_1/' + filename
    with open(path, 'r') as f:
        sql_expression = f.read()
    assert find_table_names_from_sql(sql_expression, filename) == ('test_table_1',
                                                                   ['periscope_usage_data.sql_views',
                                                                    'periscope_usage_data.sql_views1',
                                                                    'periscope_usage_data.sql_views2',
                                                                    'periscope_usage_data.sql_views3',
                                                                    'periscope_usage_data.sql_views4'])


def test_find_table_names_from_sql_file_example_2():
    filename = 'example_2.sql'
    path = test_files_dir + 'examples_2/' + filename
    with open(path, 'r') as f:
        sql_expression = f.read()
    assert find_table_names_from_sql(sql_expression, filename) == ('test_2',
                                                                   ['test.test_a', 'test.test_a1', 'test.test_c',
                                                                    'test.test_d', 'test_table_1'])


def test_find_table_names_from_sql_file_example_3():
    filename = 'example_3.sql'
    path = test_files_dir + 'examples_3/' + filename
    with open(path, 'r') as f:
        sql_expression = f.read()
    assert find_table_names_from_sql(sql_expression, filename) == ('example_3',
                                                                   ['periscope_usage_data.charts',
                                                                    'periscope_usage_data.csv',
                                                                    'periscope_usage_data.dashboards',
                                                                    'periscope_usage_data.sql_views'])
