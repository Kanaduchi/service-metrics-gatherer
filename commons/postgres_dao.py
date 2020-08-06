"""
* Copyright 2019 EPAM Systems
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
"""
import logging
import psycopg2

logger = logging.getLogger("metricsGatherer.postgres_dao")

class PostgresDAO:

    def __init__(self, app_settings):
        self.app_settings = app_settings

    def query_db(self, query, query_all=True):
        try:
            logger.info("Started query...")
            connection = psycopg2.connect(user=self.app_settings["postgresUser"],
                                          password=self.app_settings["postgresPassword"],
                                          host=self.app_settings["postgresHost"],
                                          port=self.app_settings["postgresPort"],
                                          database=self.app_settings["postgresDatabase"])

            cursor = connection.cursor()
            cursor.execute(query)
            if query_all:
                return cursor.fetchall()
            return cursor.fetchone()

        except (Exception, psycopg2.Error) as error:
            logger.error("Error while connecting to PostgreSQL %s", error)
        finally:
            if(connection):
                cursor.close()
                connection.close()

    def get_column_names_for_table(self, table_name):
        return self.query_db(
            "select column_name, data_type from information_schema.columns where table_name = '%s';"%table_name)

    def get_auto_analysis_attribute_id(self):
        return self.query_db(
            "select id, name from attribute where name = 'analyzer.isAutoAnalyzerEnabled'", query_all=False)[0]

