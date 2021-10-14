import tableauserverclient as TSC

tableau_auth = TSC.TableauAuth('sachin.ullattil@beinex.com', 'Pass@word123', 'beinexconsulting')
server = TSC.Server('https://eu-west-1a.online.tableau.com/')

with server.auth.sign_in(tableau_auth):
    # all_views, pagination_item = server.sites.get()
    # for view in all_views:
    #     print(view.name, view.id)


    a_site = server.sites.get_by_name("Beinex Consulting")
    print(a_site.id)

    # for item in TSC.Pager(server.sites):
    #     print(item.name,"  :  ",item.id)

    # all_sites, pagination_item = server.sites.get()
    #
    # # print all the site names and ids
    # for site in all_sites:
    #     print(site.id, site.name, site.content_url, site.state)
    #

    # site = server.sites.get_by_name('Beinex Consulting')
    # print(site.id, site.name, site.content_url, site.state)
