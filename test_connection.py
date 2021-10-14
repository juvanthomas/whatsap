import tableauserverclient as TSC

tableau_auth = TSC.TableauAuth('ADMIN-USERNAME', 'ADMIN-PASSWORD' )
server = TSC.Server('YOUR-URL')

with server.auth.sign_in(tableau_auth):


    all_sites, pagination_item = server.sites.get()

    # print all the site names and ids
    for site in all_sites:
        print(site.id, site.name, site.content_url, site.state)
