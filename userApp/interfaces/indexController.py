from flask import render_template, request, redirect, jsonify
from userApp import *
from userApp.database import *


def page_len(clinics):
    p_len = 0
    if len(clinics) % 50 != 0:
        p_len = int(len(clinics) / 50) + 1
    else:
        p_len = int(len(clinics) / 50)
    return p_len


def reg_filter(region):
    clinics = []
    for r in region:
        clinics = [*clinics, *Clinic.query.filter_by(clinic_region=int(r['value']))]
    return clinics


def spec_filter(special, clinics):
    clinic = []
    for s in special:
        for i in clinics:
            if i.specialization == s['value']:
                clinic.append(i)
    return clinic


def type_filter(type, clinics):
    res=[]
    for t in type:
        if t['value'] == 'Частная организация':
            for cl in clinics:
                if cl.is_private:
                    res.append(cl)
        else:
            for cl in clinics:
                if not cl.is_private:
                    res.append(cl)
    return res


def get_filtered_mo(clinics, pageNum):
    mo = []
    for i in range(len(clinics)):
        if ((pageNum - 1) * 50) < i <= (((pageNum - 1) * 50) + 50):
            mo.append(clinics[i].serialize())
        if i > (((pageNum - 1) * 50) + 50):
            break
    return mo


def send_dict(clinics, pageNum):
    mo = get_filtered_mo(clinics, pageNum)
    p_len = page_len(clinics)
    ans = [{'array': mo, 'page_len': p_len}]
    return ans


def get_all_regions_dict():
    dictionary = {}
    regions = Region.query.all()
    for el in regions:
        dictionary[f'{el.id}'] = el.region_name
    return dictionary


def get_all_specializations():
    clinics = Clinic.query.all()
    spec = set()
    for el in clinics:
        spec.add(el.specialization)
    return list(spec)


@userApp.route('/', methods=['GET', 'POST'])
@userApp.route('/page/<int:page>', methods=['GET', 'POST'])
def index():
    dictionary = get_all_regions_dict()
    regions = Region.query.all()
    clinics = Clinic.query.all()
    if request.method == 'POST':
        d = request.json
        region = d['filterRegion']
        special = d['filterSpecialization']
        type = d['filterClinicType']
        pageNum = int(d['pageNum'])
        if len(region)>0:
            clinics = reg_filter(region)
        if len(special)>0:
            clinics = spec_filter(special, clinics)
        if len(type)>0:
            clinics = type_filter(type, clinics)
        return jsonify(send_dict(clinics, pageNum))
    return render_template('index.html', regions=regions, dictionary=dictionary, spec=get_all_specializations(), false=False)


@userApp.route('/lpr')
def lpr(page=1):
    d = get_all_regions_dict()
    regions = Region.query.all()
    lpr = DecisionMaker.query.all()
    pos=set()
    for el in lpr:
        pos.add(el.position)
    return render_template('lpr.html', regions=regions, pos=pos, lpr=lpr, nan='NaN', reg=d)



def get_private(x):
    if x == 'Частная организация' or x=='Частная':
        return True
    return False


@userApp.route('/add_mo', methods=['GET', 'POST'])
def mo():
    regions = Region.query.all()  # Загрузка
    if request.method=='POST':
        try:
            name = request.form['legal_name']
            short_name = request.form['short_name']
            legal_adress = request.form['legal_adress']
            clinic_region = request.form['region']
            is_private = get_private(request.form['private'])
            specialization = request.form['spec']
            leader = request.form['leader']
            phone_numbers = request.form['phone']
            mail = request.form['mail']
            nets = request.form['nets']
            inn = request.form['inn']
            partner = False
            if request.form.get('partner') == 'on':
                partner = True
            mo = Clinic(name=name, short_name=short_name, clinic_legal_address=legal_adress, clinic_region=clinic_region,
                        is_private=is_private, specialization=specialization, leader=leader, phone_numbers=phone_numbers,
                        mail=mail, nets=nets, inn=inn, partner=partner)
            db.session.add(mo)
            db.session.commit()
            return redirect('/')
        except:
            return 'Something went wrong'
    return render_template('add_mo.html', regions=regions)


@userApp.route('/add_dm', methods=['GET', 'POST'])
def dm():
    regions = Region.query.all()  # Загрузка
    if request.method=='POST':
        try:
            name = request.form['name']
            region = request.form['region']
            pos = request.form['pos']
            phone = request.form['phone']
            nets = request.form['nets']
            mail = request.form['mail']
            tg = request.form['tg']
            vk = request.form['vk']
            fb = request.form['fb']
            ok = request.form['ok']
            dm = DecisionMaker(name=name, position=pos, dm_region=region, dm_phone=phone, dm_site=nets,
                        dm_mail=mail, dm_tg=tg, dm_vk=vk, dm_facebook=fb, dm_ok=ok)
            db.session.add(dm)
            db.session.commit()
            return redirect('/lpr')
        except:
            return 'Something went wrong'
    return render_template('add_dm.html', regions=regions)


@userApp.route('/mo/<int:id>/edit', methods=['GET', 'POST'])
def edit_mo(id):
    mo = Clinic.query.get(id)
    if request.method == 'POST':
        try:
            mo.name = request.form['legal_name']
            mo.short_name = request.form['short_name']
            mo.clinic_legal_adress = request.form['legal_adress']
            mo.clinic_region = request.form['region']
            mo.is_private = get_private(request.form['private'])
            mo.specialization = request.form['spec']
            mo.leader =request.form['leader']
            mo.phone_numbers = request.form['phone']
            mo.mail = request.form['mail']
            mo.nets = request.form['nets']
            mo.inn = request.form['inn']
            if request.form.get('partner') == 'on':
                mo.partner = True
            else:
                mo.partner = False
            db.session.commit()
            return redirect('/')
        except:
            return 'Something went wrong with db'
    regions = Region.query.all()
    return render_template('update_mo.html', mo=mo, regions=regions)


@userApp.route('/dm/<int:id>/edit', methods=['GET','POST'])
def edit_dm(id):
    dm = DecisionMaker.query.get(id)
    regions = Region.query.all()
    if request.method=='POST':
        try:
            dm.name = request.form['name']
            dm.dm_region = request.form['region']
            dm.position = request.form['pos']
            dm.dm_phone = request.form['phone']
            dm.dm_site = request.form['nets']
            dm.dm_mail = request.form['mail']
            dm.dm_tg = request.form['tg']
            dm.dm_vk = request.form['vk']
            dm.dm_fb = request.form['fb']
            dm.dm_ok = request.form['ok']
            db.session.commit()
            return redirect('/lpr')
        except:
            return 'Something went wrong'
    return render_template('update_dm.html', dm=dm, regions=regions)


@userApp.route('/dm/<int:id>/del')
def del_dm(id):
    try:
        db.session.delete(DecisionMaker.query.get(id))
        db.session.commit()
        return 'nice'
    except:
        return 'Something went wrong'


@userApp.route('/mo/<int:id>/del')
def del_mo(id):
    try:
        db.session.delete(Clinic.query.get(id))
        db.session.commit()
        return 'nice'
    except:
        return 'Something went wrong'

