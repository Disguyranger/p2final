d3.json('/api/data/property_type_price').then(data => {


    cities = data.map(d => d.City);
    single_family_avg_price = data.map(d => d.SingleFamilyAvgPrice);
    condo_avg_price = data.map(d => d.CondoAvgPrice);
    townhouse_avg_price = data.map(d => d.TownhouseAvgPrice);
        
    var single_family_trace = {
      y: single_family_avg_price,
      x: cities,
      type: 'bar',
      name: 'Single Family',
      text: single_family_avg_price.map(String),
      textposition: 'auto',
      hoverinfo: 'none',
      opacity: 0.5,
      orienation: 'h',
      marker: {
        color: 'rgb(158,202,225)',
        line: {
          color: 'rgb(8,48,107)',
          width: 1.5
        }
      }
    };
    
    var condo_trace = {
      y: condo_avg_price,
      x: cities,
      type: 'bar',
      name: 'Condo',
      text: condo_avg_price.map(String),
      textposition: 'auto',
      hoverinfo: 'none',
      orienation: 'h',
      marker: {
        color: 'rgba(58,200,225,.5)',
        line: {
          color: 'rgb(8,48,107)',
          width: 1.5
        }
      }
    };

    var townhouse_trace = {
        y: townhouse_avg_price,
        x: cities,
        type: 'bar',
        name: 'Townhouse',
        text: townhouse_avg_price.map(String),
        textposition: 'auto',
        hoverinfo: 'none',
        orienation: 'h',
        marker: {
          color: 'rgba(88,140,192,.5)',
          line: {
            color: 'rgb(8,48,107)',
            width: 1.5
          }
        }
      };
    
    var data = [single_family_trace,condo_trace,townhouse_trace];
    
    var layout = {
      title: 'Average Selling Prices'
    };
    
    Plotly.newPlot('avg_selling_prices_group', data, layout);
});




d3.json('/api/data/city_type_price').then(data => {
    
    property_type = data.map(d => d.PropertyType);
    city = data.map(d => d.City);
    property_type_and_city = data.map(d => `${d.PropertyType} / ${d.City}`);
    avg_price = data.map(d => d.AveragePrice);
    
    var avg_price_trace = {
    y: property_type_and_city,
    x: avg_price,
    type: 'bar',
    text: avg_price.map(String),
    name: 'Average Selling Price',
    textposition: 'auto',
    hoverinfo: 'none',
    orientation: 'h',
    marker: {
        color: 'rgb(158,202,225)',
        opacity: 0.6,
        line: {
        color: 'rgb(8,48,107)',
        width: 1.5
        }
    }
    };

    var data = [avg_price_trace];

    var layout = {
    title: 'Average Selling Price by Property Type and City',
    //barmode: 'stack'
    };

    Plotly.newPlot('avg_price_bar', data, layout);

});