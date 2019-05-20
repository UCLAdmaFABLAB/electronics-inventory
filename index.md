---
---
{% assign types = site.data.manifest.inventory | group_by: 'type' %}
<h2>Drawers</h2>
<ul class='contents'>
{% for type in types %}
  <li><a href='#{{ type.name}}'>{{ type.name  }}</a></li>
{% endfor %}
</ul>

<hr />

{% for type in types %}
  <h3 id='{{type.name}}'>{{ type.name | capitalize }}</h3>
  <table class='inventory'>
    <tr>
      <th></th>
      <th>Title</th>
      <th>Size</th>
      <th>Quantity</th>
    </tr>
    <tbody>
    {% for item in type.items %}
      <tr>
        <td>
          <img src="{{ site.baseurl }}/images{{ item.image }}" />
        </td>
        <td>
          <h4>{{ item.title }}</h4>
          {% if item.subtitle %}
            <h4 class="subtitle">{{item.subtitle}}</h4>
          {% endif %}
        </td>
        <td>
          {{ item.size }}
        </td>
        <td>
          {{ item.quantity }}
        </td>
      </tr>
    {% endfor %}
    </tbody>
  </table>
{% endfor %}
