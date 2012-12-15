// Generated by CoffeeScript 1.3.3
(function() {

  $(function() {
    var $form, $identifier, $result, activeRequest, cacheResponse, doService, getActiveService, hashRequest, lastQuery, parseFormData, renderError, renderResponse, renderResult, renderSucces, requestCache, sendRequest, services, setIdentifer, waitingPanda;
    $form = $('form.remindergram');
    $identifier = $('#identifier');
    $result = $('.result');
    services = {
      'Instagram': 'Username',
      'WordPress': 'Blog address',
      'Tumblr': 'Blog address',
      'RSS': 'Feed address'
    };
    activeRequest = false;
    lastQuery = {};
    requestCache = {};
    $form.find('.btn').on('click', function(event) {
      event.preventDefault();
      $form.find('.btn').removeClass('active');
      $(this).addClass('active');
      doService($(event.target).text());
      return $identifier.focus();
    });
    getActiveService = function() {
      var active;
      active = $form.find('.btn.active');
      if (active) {
        return active.text();
      } else {
        return '';
      }
    };
    doService = function(name) {
      return setIdentifer(services[name]);
    };
    setIdentifer = function(placeholder) {
      $('label[for="identifier"]').text("Enter " + placeholder);
      return $identifier.attr('placeholder', placeholder);
    };
    $form.on('submit', function(event) {
      var data, hash;
      event.preventDefault();
      data = parseFormData($form);
      if (_.contains(_.values(data), '')) {
        return;
      }
      if (_.isEqual(data, this.lastQuery)) {
        return;
      }
      this.lastQuery = data;
      hash = hashRequest(data);
      if (_.has(requestCache, hash)) {
        return renderResponse(requestCache[hash]);
      }
      if (this.activeRequest) {
        this.activeRequest.abort();
      }
      return this.activeRequest = sendRequest(data);
    });
    hashRequest = function(data) {
      return _.pairs(data).toString();
    };
    sendRequest = function(data) {
      waitingPanda();
      return $.post($form.attr('action'), data, function(response) {
        cacheResponse(data, response);
        return renderResponse(response);
      });
    };
    renderResponse = function(response) {
      if (response.error) {
        return renderError(response);
      } else {
        return renderSucces(response);
      }
    };
    cacheResponse = function(data, response) {
      var hash;
      hash = hashRequest(data);
      return requestCache[hash] = response;
    };
    $form.keyup(_.debounce(function() {
      return $form.submit();
    }, 800));
    parseFormData = function($form) {
      var inputs;
      inputs = _.reduce($form.serializeArray(), function(data, pair) {
        data[pair.name] = pair.value;
        return data;
      }, {});
      return _.extend(inputs, {
        'service': getActiveService()
      });
    };
    renderSucces = function(response) {
      var compiled;
      compiled = _.template('\
			<ul>\
			<% _.each(photos, function(photo) { %>\
				<li><div class="crop"><img src="<%= photo %>"></div></li> <%\
			}); %>\
			</ul>', {
        photos: response
      });
      return renderResult(compiled);
    };
    renderError = function(response) {
      var compiled;
      compiled = _.template('Oops, there was an error: <%= error %>', response);
      return renderResult(compiled);
    };
    renderResult = function(html) {
      return $result.html(html);
    };
    return waitingPanda = function() {
      var compiled;
      compiled = _.template('<p class="waiting"><img src="<%= src %>" class="waiting-panda">  Red pandas are fetching your images ...</p>', {
        src: 'http://25.media.tumblr.com/tumblr_ly2em98lub1r3m4cbo1_400.gif'
      });
      return _.debounce(renderResult(compiled), 500);
    };
  });

}).call(this);
