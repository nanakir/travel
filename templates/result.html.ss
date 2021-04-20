<!-- extend from base layout -->
{% extends "login.html" %}
{% block content %}
  <h1>Fly Results Between {{ form.minusd.data }} USD and {{ form.maxusd.data }} USD Departing {{ form.iata.data.upper() }}</h1>
     <p>
    {% for x in quotes %}
        {% if x["MinPrice"] > form.minusd.data and x["MinPrice"] < form.maxusd.data and x["OutboundLeg"]["CarrierIds"] %}
            <p>QUOTE ID: {{ x["QuoteId"] }}<br>
               PRICE: {{ x["MinPrice"] }}<br>
               DIRECT: {{ x["Direct"] }}<br>
               AIRLINE CODE: {{ x["OutboundLeg"]["CarrierIds"][0] }}<br>
               ORIGIN CODE: {{ x["OutboundLeg"]["OriginId"] }}<br>
               DESTINATION CODE: {{ x["OutboundLeg"]["DestinationId"] }}<br>
               FLY OUT/FLY IN/CHECK D: {{ x["OutboundLeg"]["DepartureDate"] }} | {{ x["InboundLeg"]["DepartureDate"] }} | {{ x["QuoteDateTime"] }}
            </p>
            {% for p in places %}
                {% if x["OutboundLeg"]["OriginId"] == p["PlaceId"] %}
                    <p>ORIGIN CODE: {{ p["PlaceId"]}}<br>
                       AIRPORT: {{ p["IataCode"] }}<br>
                       CITY: {{ p["CityName"] }}<br>
                       COUNTRY: {{ p["CountryName"] }}
                    </p>
                {% endif %}
            {% endfor %}
            {% for p in places %}
                {% if x["OutboundLeg"]["DestinationId"] == p["PlaceId"] %}
                    <p>DESTINATION CODE: {{ p["PlaceId"]}}<br>
                       AIRPORT: {{ p["IataCode"] }}<br>
                       CITY: {{ p["CityName"] }}<br>
                       COUNTRY: {{ p["CountryName"] }}
                    </p>
                {% endif %}
            {% endfor %}
            {% for c in carriers %}
                {% if x["OutboundLeg"]["CarrierIds"][0] == c["CarrierId"] %}
                    <p>AIRLINE CODE: {{ c["CarrierId"] }}<br>
                       AIRLINE: {{ c["Name"] }}
                    </p>
                {% endif %}
            {% endfor %}
            <hr>
        {% endif %}
    {% endfor %}
      </p>
  </form>
{% endblock %}
