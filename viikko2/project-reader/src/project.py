class Project:
    def __init__(self, name, description, prod_license, authors, dependencies, dev_dependencies):
        self.name = name
        self.description = description
        self.license = prod_license
        self.authors = authors
        self.dependencies = dependencies
        self.dev_dependencies = dev_dependencies

    def _stringify_dependencies(self, dependencies):
        return ", ".join(dependencies) if len(dependencies) > 0 else "-"
    
    def list_results(self, list):
        text = ""
        for i in list:
            text += (f"\n - {i}")
        return text

    def __str__(self):
        return (
            f"Name: {self.name}"
            f"\nDescription: {self.description or '-'}"
            f"\nLicense:: {self.license or '-'}"
            f"\n\nAuthors: {self.list_results(self.authors)}"
            f"\n\nDependencies: {self.list_results(self.dependencies)}"
            f"\n\nDevelopment dependencies: {self.list_results(self.dev_dependencies)}"
        )
