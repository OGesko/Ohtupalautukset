from urllib import request
from project import Project
import toml


class ProjectReader:
    def __init__(self, url):
        self._url = url

    def get_project(self):
        # tiedoston merkkijonomuotoinen sisältö
        content = request.urlopen(self._url).read().decode("utf-8")
        #print(content)

        # deserialisoi TOML-formaatissa oleva merkkijono ja muodosta Project-olio sen tietojen perusteella
        data = toml.loads(content)
        #print(data)
        udata = data.get("tool").get("poetry")
        name = udata.get("name")
        description = udata.get("description")
        prod_license = udata.get("license")
        authors = udata.get("authors")
        dependencies = udata.get("dependencies").keys()
        dev_dependencies = udata.get("group").get("dev").get("dependencies").keys()
        return Project(name, description, prod_license, authors, dependencies, dev_dependencies )
