// Generated by CoffeeScript 1.4.0
(function() {

  $(function() {
    var $form, $identifier, $result, $service, destroyService, doService, parseFormData, renderError, renderResult, renderSucces, services, setIdentifer, waitingPanda;
    $form = $('form.remindergram');
    $service = $('#service');
    $identifier = $('#identifier');
    $result = $('.result');
    services = {
      'Instagram': 'Username',
      'WordPress': 'Blog address',
      'RSS': 'Feed address'
    };
    $service.on('keyup', function(event) {
      var $val;
      $val = $(event.target).val();
      if (services.hasOwnProperty($val)) {
        return doService($val);
      } else {
        return destroyService();
      }
    });
    doService = function(name) {
      return setIdentifer(services[name]);
    };
    destroyService = function() {
      return setIdentifer('');
    };
    setIdentifer = function(placeholder) {
      return $identifier.attr('placeholder', placeholder);
    };
    $form.on('submit', function(event) {
      var data, timer;
      event.preventDefault();
      data = parseFormData($form);
      timer = waitingPanda();
      return $.post($form.attr('action'), data, function(response) {
        clearTimeout(timer);
        if (response.error) {
          return renderError(response);
        } else {
          return renderSucces(response);
        }
      });
    });
    parseFormData = function($form) {
      return _.reduce($form.serializeArray(), function(data, pair) {
        data[pair.name] = pair.value;
        return data;
      }, {});
    };
    renderSucces = function(response) {
      var compiled;
      compiled = _.template("<% _.each(photos, function(photo) { %> <li><img src='<%= photo %>'</li> <% }); %>", {
        photos: response
      });
      return renderResult(compiled);
    };
    renderError = function(response) {
      var compiled;
      compiled = _.template("Oops, there was an error: <%= error %>", response);
      return renderResult(compiled);
    };
    renderResult = function(html) {
      return $result.html(html);
    };
    return waitingPanda = function() {
      var compiled;
      compiled = _.template("<img src='<%= src %>'>", {
        src: 'http://25.media.tumblr.com/tumblr_ly2em98lub1r3m4cbo1_400.gif'
      });
      return setTimeout(function() {
        return renderResult(compiled);
      }, 500);
    };
  });

}).call(this);
