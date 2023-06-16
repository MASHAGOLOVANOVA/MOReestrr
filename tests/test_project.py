from userApp.database import *


def test_add_mo(client, app):
    count = Clinic.query.count()
    response = client.post("/add_mo", data={"legal_name": "LEGAL", "short_name": "SHORT", "leader": "LEADER",
                                            "region": 10, "private": 1, })
    with app.app_context():
        assert Clinic.query.count() != count+1


def test_add_mo_successfull(client, app):
    count = Clinic.query.count()
    try:
        response = client.post("/add_mo", data={"short_name": "SHORT", "leader": "LEADER", "region": 10, "private": 1, })
    except:
        pass
    with app.app_context():
        assert Clinic.query.count() == count


def test_add_dm(client, app):
    count = DecisionMaker.query.count()
    response = client.post("/add_dm", data={"name": "LEGAL    ", "position": "SHORT", "leader": "LEADER",
                                            "region": 10, "private": 1, })
    with app.app_context():
        assert DecisionMaker.query.count() != count+1


def test_add_mo_unsuccessfull(client, app):
    count = Clinic.query.count()
    try:
        response = client.post("/add_mo", data={"short_name": "SHORT", "leader": "LEADER", "region": 10, "private": 1, })
    except:
        pass
    with app.app_context():
        assert Clinic.query.count() == count


def test_del_mo(client,app):
    count = Clinic.query.count()
    client.get("/mo/21/del")
    with app.app_context():
        assert Clinic.query.count() == count-1


def test_del_dm(client,app):
    count = DecisionMaker.query.count()
    client.get("/dm/226/del")
    with app.app_context():
        assert DecisionMaker.query.count() == count-1


def test_edit_dm(client, app):
    client.post("/dm/20/edit", data={"name": "XXX"})
    with app.app_context():
        assert DecisionMaker.query.get(20).name=='XXX'


def test_edit_mo(client, app):
    client.post("/mo/46/edit", data={"legal_name": "XXX"})
    with app.app_context():
        assert Clinic.query.get(46).name =='XXX'


def test_mos_open(client):
    response = client.get("/")
    assert response.status_code==200


def test_lpr_open(client):
    response = client.get("/lpr")
    assert response.status_code==200
