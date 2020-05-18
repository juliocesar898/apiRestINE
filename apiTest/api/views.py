
from django.db import connections
from rest_framework import viewsets
from rest_framework.response import Response

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class CreateTableView(viewsets.ViewSet):
    """
    API Endpoint for create tables
    """
    def create(self, request):
        message = ''
        nameTab = request.data['name_tab']
        fields = request.data['fields']

        sql = ("CREATE TABLE IF NOT EXISTS "+nameTab+" ")

        
        constrains = []
        for key in fields.keys():
            constrains.append(str(key)+' '+str(fields[key]['field_type']))

        complement = ', '.join( str(a) for a in constrains )

        sql += "( "+str(complement)+" );"

        c = connections['default'].cursor()
        try:
            c.execute(sql)
            message = "Done... The Table "+nameTab+" has been created!!!"
        except:
            message = "Failed Operation"
        finally:
            c.close()

        return Response(message)

class InsertDataView(viewsets.ViewSet):
    """
    API Endpoint for insert registers into tables
    """
    def create(self, request):
        message = ''
        sql = ''
        fields_complement = ''
        values_complement = ''

        nameTab = request.data['name_tab']
        record = request.data['record']

        sql = ("INSERT INTO "+nameTab+" ")

        fields = []
        values = []

        for key in record.keys():
            fields.append(key)
            values.append(record[key])

        fields_complement = ', '.join( str(a) for a in fields )

        for a in values:
            values_complement += " '"+str(a)+"', " if type(a) == str \
                else " "+str(a)+", "

        sql += ("( "+fields_complement+" ) VALUES ( "+
                values_complement[:-2]+" );") 

        c = connections['default'].cursor()
        try:
            c.execute(sql)
            message = "Done... The record has been inserted on "+nameTab
        except:
            message = "Failed Operation"
        finally:
            c.close()

        return Response(message)

class GetDataView(viewsets.ViewSet):
    """
    API Endpoint for get datasets from tables
    """
    def list(self, request):

        message = ''
        dataset = []

        nameTab = request.data['name_tab']
        fields = request.data['fields']

        sql = ("SELECT "+', '.join( str(a) for a in fields )+
                +" FROM "+nameTab+";")

        c = connections['default'].cursor()
        try:
            c.execute(sql)
            dataset = dictfetchall(c)
        except:
            dataset.append('Failed Operation')
        finally:
            c.close()
        return Response(dataset)

class ListTablesView(viewsets.ViewSet):
    """
    API Endpoint fot list all the tables
    """
    def list(self, request):

        dataset = []

        sql = ("select table_name from information_schema.tables"+
                " where table_schema = 'public';")

        c = connections['default'].cursor()
        try:
            c.execute(sql)
            dataset = dictfetchall(c)
        except:
            dataset.append('Failed Operation')
        finally:
            c.close()
        return Response(dataset)

class InfoTableView(viewsets.ViewSet):
    """
    API Endpoint for get info tables
    """
    def list(self, request):

        nameTab = request.data['name_tab']

        sql = ("SELECT table_name, column_name, data_type, udt_name FROM "+
            "information_schema.columns "+
            "WHERE table_schema = 'public' AND table_name   = '"+nameTab+"';")

        c = connections['default'].cursor()
        try:
            c.execute(sql)
            dataset = dictfetchall(c)
        except:
            dataset.append('Failed Operation')
        finally:
            c.close()
        return Response(dataset)

class DeleteTableView(viewsets.ViewSet):

    def create(self, request):

        message = ''
        nameTab = request.data['name_tab']

        sql = ("DROP TABLE IF EXISTS "+nameTab+";")

        c = connections['default'].cursor()
        try:
            c.execute(sql)
            message = 'Done... the table '+nameTab+' has deleted'
        except:
            message = 'An error has ocurred!'
        finally:
            c.close()
        return Response(message)