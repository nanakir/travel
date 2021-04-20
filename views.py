from flights import flights
from flights import db, models
from datetime import datetime, date
from flask import render_template, flash, redirect, json, jsonify, request, url_for
from .forms import LoginForm
from js.jquery import jquery
from js.bootstrap_datepicker import bootstrap_datepicker
from flask_fanstatic import Fanstatic
from collections import OrderedDict
from time import sleep
import requests, json, time, numpy, concurrent.futures

dbiatadata = models.Qpxiata
NAMES=['one','two','three','four']
opulence = 1 

@flights.route('/demo', methods=['GET', 'POST'])
def test():
    print("Delivered")
    return render_template('index.html')


@flights.route('/autocomplete', methods=['GET'])
def autocomplete():
    s = {}
    x = []
    s_new = []
    search = ''
    print(type(search.isalpha()))
    if request.args.get('term'):
        search = request.args.get('term')
        if search.isalpha():
            print("Entered Main Loop")
            for i in dbiatadata.query.filter(models.Qpxiata.description.like('%{}%'.format(search))).all():
                print(i.description)
                s[i.iata]=i.description
            for key, value in s.items():
                print(key, "and", value)
                x.append({"value": key, "label": value})
 
    s_new = json.dumps(x, sort_keys=True, indent=4, ensure_ascii=False)
    print(s_new)
    # Testing purposes
    print("JJJJJJJJJJJJJJJJ", type(s_new))
    json_list = s_new
    return json_list

@flights.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    resultf = open('qpxjsonout', 'w')
    if request.method == "POST":
        if form.validate_on_submit():
            def qpxresponse():
                counter = 0
                counter2 = 0
                error = 0
                flightindex = OrderedDict()
                eastregion = ['JAX', 'MIA', 'ATL', 'BOS', 'JFK', 'CLT', 'MCO', 'EWR', 'PHL', 'LGA', 'FLL', 'BWI', 'DCA', 'ORL', 'TPA']
                centralregion = ['STL', 'DFW', 'ORD', 'DTW', 'MSP', 'IAH', 'MDW']
                mountainregion = ['DEN', 'LAS', 'RNO', 'PHX', 'SLC']
                pacificregion = ['PDX', 'SFO', 'LAX', 'SEA', 'SAN', 'HNL']
                origin = form.iata.data.upper()
                def load_qpx(region):
                    origin = form.iata.data.upper()
                    print(" LOADER REGION:       ", region)
                    if opulence == 0:
                        x = json.loads(requests.post('https://www.googleapis.com/qpxExpress/v1/trips/search?key=invalid', json = {"request": {"slice": [{"origin": "%s" %(origin),"destination": "%s" %(region),"date": "%s" %(form.flyoutdate.data.strftime("%Y-%m-%d")),"preferredCabin": "COACH"}],"passengers": {"adultCount": 1,"infantInLapCount": 0,"infantInSeatCount": 0,"childCount": 0,"seniorCount": 0},"solutions": 5,"refundable": "false"}}).text)
                    else:
                        x = json.loads(requests.post('https://www.googleapis.com/qpxExpress/v1/trips/search?key=invalid', json = {"request": {"slice": [{"origin": "%s" %(origin),"destination": "%s" %(region),"date": "%s" %(form.flyoutdate.data.strftime("%Y-%m-%d")),"preferredCabin": "FIRST"}],"passengers": {"adultCount": 1,"infantInLapCount": 0,"infantInSeatCount": 0,"childCount": 0,"seniorCount": 0},"solutions": 5,"refundable": "false"}}).text)
                    return x
                if form.region.data == 'east':
                    region = eastregion
                if form.region.data == 'central':
                    region = centralregion
                if form.region.data == 'mountain':
                    region = mountainregion
                if form.region.data == 'pacific':
                    region = pacificregion
                print("REGION BEFORE PROCESSING:            ",region)

                if origin in region:
                    print("FOUND ORIGIN IN LIST")
                    region.remove(origin)
                    print("REGION AFTER PROCESSING:            ",region)
                with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
                    future_qpx = {executor.submit(load_qpx, region): region for region in region}
                    results = concurrent.futures.wait(future_qpx, timeout=20)
                for future in results.done:
                    d = future.result()
                    print("EVERYTHING", d)
                    x = 0
                    try:
                        trip = d['trips']['tripOption']
                    except:
                        print("Key Value Failed. No flight")
                        #break
                        continue
                    for t in trip: 
                        if opulence == 1:
                            isFirst = 1
                            while x != len(t["slice"]) and isFirst != 0: 
                                y = 0
                                while y != len(t["slice"][x]["segment"] or isFirst == 0):
                                    if t["slice"][x]["segment"][y]["cabin"] == "COACH":
                                        print("FOUND A COACH ON:", t["id"], "AT SEGMENT", y)
                                        print("**** HALTING TRIP PARSE ****")
                                        isFirst = 0
                                        y += 1
                                        continue
                                    else:
                                        print("NO COACH FOUND ON:", t["id"], "AT SEGMENT", y, file = resultf)
                                        print("**** CONTINUE ****")
                                    y += 1
                                x += 1
                            else:
                                print(t["id"], "GOES INTO MAIN LOOP - PROCESSING")
                            #
                            # Now we continue with our main loop
                            #
                        y = 0
                        x = 0
                        counter += 1
                                    #
                                    # Eval the number of segments - a segment is an action - origin to destination
                                    #
                        while y != len(t["slice"][x]["segment"]):
                            print("This is slice:", x, "of:", t["id"], "priced", t["saleTotal"], sep='\t', file = resultf)
                            qpxprice = t["saleTotal"]
                            qpxflightid = t["id"]
                            print("Y counter is: ", y, file=resultf)
                            print("X counter is: ", x, file=resultf)
                            print("There are", len(t["slice"][x]["segment"]), "segments on this flight", file=resultf)
                            print("There are", len(t["slice"][x]["segment"][y]["leg"]), "legs per segment", file = resultf)
                            z = 0
                            while z != len(t["slice"][x]["segment"][y]["leg"]):
                                print("Leg:", z, "on flight", t["slice"][x]["segment"][y]["flight"]["number"], file = resultf)
                                qpxleg =  z
                                print("Flight Number:", z, "on flight", t["slice"][x]["segment"][y]["flight"]["number"], file = resultf)
                                qpxflightname = t["slice"][x]["segment"][y]["flight"]["number"]
                                print("Departure Time:", t["slice"][x]["segment"][y]["leg"][z]["departureTime"], file = resultf)
                                qpxdeparturet = t["slice"][x]["segment"][y]["leg"][z]["departureTime"]
                                print("Arrival Time:", t["slice"][x]["segment"][y]["leg"][z]["arrivalTime"], file = resultf)
                                qpxarrivalt = t["slice"][x]["segment"][y]["leg"][z]["arrivalTime"]
                                print("Origin:", t["slice"][x]["segment"][y]["leg"][z]["origin"], file = resultf)
                                qpxorigin = t["slice"][x]["segment"][y]["leg"][z]["origin"]
                                print("Destination:", t["slice"][x]["segment"][y]["leg"][z]["destination"], file = resultf)
                                qpxdestination = t["slice"][x]["segment"][y]["leg"][z]["destination"]
                                print("Cabin:", t["slice"][x]["segment"][y]["cabin"], file = resultf)
                                qpxflightcabin = t["slice"][x]["segment"][y]["cabin"]
                                print("Leg:", z, "on flight", t["slice"][x]["segment"][y]["flight"]["number"], file = resultf)
                                print("Carrier:", t["slice"][x]["segment"][y]["flight"]["carrier"], file = resultf)
                                qpxcarrier =  t["slice"][x]["segment"][y]["flight"]["carrier"]
                                print("Y counter is: ", y, file = resultf)
                                print("X counter is: ", x, file = resultf)
                                print("Z counter is: ", z, file = resultf)
                                flightindex[qpxflightid] = qpxdestination
                                dbqpxflight = models.Qpxflight(qpxflightname)
                                dbqpxflightdata = models.Qpxflightdata(qpxprice, qpxflightid, qpxleg, qpxdeparturet, qpxarrivalt, qpxorigin, qpxdestination, qpxflightcabin, qpxcarrier, dbqpxflight)
                                db.session.add(dbqpxflight, dbqpxflightdata)
                                z += 1
                            y += 1 
                            print()
                        x += 1
                        #j += 1
                        #print("MAIN LOOP ITERATIONS: ", j)
                            #else:
                            #    flash('No Opulent Flights') 
                            #    err = "No Opulent Flights Found"
                            #    return render_template('login.html', title='Enter Airport Code ex. DIA JAX SEA', form=LoginForm(), error=err)
                            # end region for loop
                        print(" -------------- END MAIN LOOP -------------")
                    print("OUTER LOOP:        ", counter2)
                    counter2 += 1
                db.session.commit()
                dbqueryobj = db.session.query(models.Qpxflightdata).join(models.Qpxflight)
                dbqpxflightdata = models.Qpxflightdata
                dbqpxflight = models.Qpxflight
                return render_template('result.html', title='Results',form=form, dbqueryobj=dbqueryobj, flightindex=flightindex, dbqpxflight=dbqpxflight, dbqpxflightdata=dbqpxflightdata, origin=origin, counter=counter)
            #
            # Qpx function end
            #
            return flights.response_class(qpxresponse(), content_type='text/html')
        #
        # Closes validate function if
        #
        else:
            flash('Please Check Input Fields') 
            err = "Please Check The Input Fields"
            return render_template('login.html', title='Enter Airport Code ex. DIA JAX SEA', form=LoginForm(), error=err)
            #return render_template('login.html', title='Enter Airport Code ex. DIA JAX SEA', form=LoginForm(), error=err)
            #return redirect(url_for('login'))
    #
    # Closes Main IF statement - Check for POST
    #
    return render_template('login.html', title='Enter Airport Code ex. DIA JAX SEA', form=LoginForm())
