import tableauserverclient as TSC

tableau_auth = TSC.TableauAuth('beinexadmin', 'Bein3x@987','Expo')

server = TSC.Server('http://61.2.141.81:8080')
#server = TSC.Server('https://analytics.beinex.com/')

#server.version = '3.8'

with server.auth.sign_in(tableau_auth):
    all_datasources, pagination_item = server.datasources.get()
#   print("\nSite id  {} :".format(id))
#    print(id)
#    print("\nThere are {} datasources on site: ".format(pagination_item.total_available))
#    print([datasource.name for datasource in all_datasources])
    print(server.version)
    print("##############  Views  ################")

    for x in TSC.Pager(server.views):    #change server.views or server.workbooks  etc
        print(x.name+"     "+x.id )
        
    all_sites, pagination_item = server.sites.get()
#    a_site = server.sites.get_by_name('Expo')

  # print all the site names and ids
    print("##############  Sites  ################")
    for site in all_sites:
       print(site.id, site.name, site.content_url, site.state)
