from core.universes import *


def configure_pc():
    components = Universe(Level(1))
    configs = Universe(Level(2))
    templates = Universe(Level(3))

    cpu = Type("CPU", Level(0), components)
    components.add_type("cpu", cpu)
    
    ram = Type("RAM", Level(0), components)
    components.add_type("ram", ram)
    
    gpu = Type("GPU", Level(0), components)
    components.add_type("gpu", gpu)

    office_pc = Type("office PC", Level(1), configs)
    office_pc.add_constructor(
        "new", Constructor("new", {"CPU": cpu, "RAM": ram, "GPU": gpu}))
    configs.add_type("office_pc", office_pc)
    
    top_pc = Type("top PC", Level(1), configs)
    top_pc.add_constructor(
        "new", Constructor("new", {"CPU": cpu, "RAM": ram, "GPU": gpu}))
    configs.add_type("top_pc", top_pc)
    
    home_pc = Type("home PC", Level(1), configs)
    home_pc.add_constructor(
        "new", Constructor("new", {"CPU": cpu, "RAM": ram, "GPU": gpu}))
    configs.add_type("home_pc", home_pc)

    # CPU, RAM, GPU of same generation
    coherent_template = Type("coherent", Level(2), templates)
    templates.add_type("coherent_template", coherent_template)


configure_pc()


def document_system():
    def has_access(person: Type, document: Type) -> bool:
        return person.level.value >= document.level.value

    def increase_level(document: Type) -> Type:
        return UniversePolymorphism.lift(document, +1)

    def decrease_level(document: Type) -> Type:
        return UniversePolymorphism.lift(document, -1)

    public_universe = Universe(Level(1))
    internal_universe = Universe(Level(2))
    secret_universe = Universe(Level(3))

    public_articles = Universe(Level(1))
    article = Type("Article", Level(0), public_articles)
    public_articles.add_type("article", article)

    internal_instructions = Universe(Level(2))
    instruction = Type("Instruction", Level(1), internal_instructions)
    internal_instructions.add_type("instruction", instruction)

    secret_blueprints = Universe(Level(3))
    blueprint = Type("Blueprint", Level(2), secret_blueprints)
    secret_blueprints.add_type("blueprint", blueprint)

    client = Type("Client", Level(0), public_universe)
    public_universe.add_type("client", client)
    manager = Type("Manager", Level(1), internal_universe)
    internal_universe.add_type("manager", manager)
    engineer = Type("Engineer", Level(2), secret_universe)
    secret_universe.add_type("engineer", engineer)

    assert has_access(client, article)
    assert not has_access(client, instruction)
    assert not has_access(client, blueprint)
    assert has_access(manager, article)
    assert has_access(manager, instruction)
    assert not has_access(manager, blueprint)
    assert has_access(engineer, article)
    assert has_access(engineer, instruction)
    assert has_access(engineer, blueprint)

    internal_article = increase_level(article)
    internal_blueprint = decrease_level(blueprint)

    assert not has_access(client, internal_article)
    assert has_access(manager, internal_blueprint)

document_system()


def form_validator():
    def validate_level(t: Type, lo: Optional[Level], up: Optional[Level]) -> bool:
        if lo is not None and (
            t.level.value < lo.value or
            t.universe.level.value < lo.value + 1):
            return False
        if up is not None and (
            t.level.value > up.value or
            t.universe.level.value > up.value + 1):
            return False
        return all(
            validate_level(v, None, Level(t.level.value - 1))
            for c in t.constructors.values()
            for v in c.params.values())


    def validate_form(form: Type) -> bool:
        return validate_level(form, Level(2), None)


    basic_types = Universe(Level(1))
    composite_types = Universe(Level(2))
    forms = Universe(Level(3))

    string = Type("String", Level(0), basic_types)
    basic_types.add_type("string", string)

    number = Type("Number", Level(0), basic_types)
    basic_types.add_type("number", number)

    address = Type("Address", Level(1), composite_types)
    address.add_constructor(
        "new",
        Constructor("", {"Street": string, "House": number}))
    composite_types.add_type("address", address)

    contact = Type("Contact", Level(1), composite_types)
    address.add_constructor(
        "new",
        Constructor("", {"Firstname": string, "Lastname": string}))
    composite_types.add_type("contact", contact)

    players = Type("Players", Level(2), forms)
    players.add_constructor(
        "new",
        Constructor("", {"Red": contact, "Blue": contact})
    )
    forms.add_type("players", players)

    cv = Type("CV", Level(2), forms)
    cv.add_constructor(
        "new",
        Constructor("", {"Name": contact, "Address": address})
    )
    forms.add_type("cv", cv)

    assert validate_form(players)
    assert validate_form(cv)

form_validator()
