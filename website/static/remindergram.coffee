$ ->
	# Dom elements
	$form       = $ 'form.remindergram'
	$service    = $ '#service'
	$identifier = $ '#identifier'
	$result     = $ '.result'

	# Service/identify map
	services =
		'Instagram' : 'Username'
		'WordPress' : 'Blog address'
		'RSS'       : 'Feed address'

	# Listen on service keyup
	$service.on 'keyup', ( event )->
		$val = $( event.target ).val()
		if services.hasOwnProperty $val
			doService $val
		else
			destroyService()

	doService = ( name )->
		setIdentifer services[name]

	destroyService = ->
		setIdentifer ''

	setIdentifer = ( placeholder ) ->
		$identifier.attr 'placeholder', placeholder

	# Listen on form submit
	$form.on 'submit', ( event ) ->
		event.preventDefault()

		data = parseFormData $form
		timer = waitingPanda()
		$.post $form.attr( 'action' ), data, ( response ) ->
			clearTimeout timer
			if response.error
				renderError response
			else
				renderSucces response

	# Auto-submit form when the user stops typing
	$form.keyup ->
		clearTimeout @keyup_timer
		@keyup_timer = setTimeout ->
			$form.submit()
		, 800

	parseFormData = ( $form ) ->
		return _.reduce $form.serializeArray(), ( data, pair ) ->
			data[ pair.name ] = pair.value
			return data
		, {}

	renderSucces = (response) ->
		compiled = _.template "<% _.each(photos, function(photo) { %> <li><img src='<%= photo %>'</li> <% }); %>", {photos: response}
		renderResult compiled

	renderError = ( response ) ->
		compiled = _.template "Oops, there was an error: <%= error %>", response
		renderResult compiled

	renderResult = ( html ) ->
		$result.html html

	waitingPanda = ->
		compiled = _.template "<img src='<%= src %>'>",
			src: 'http://25.media.tumblr.com/tumblr_ly2em98lub1r3m4cbo1_400.gif'

		setTimeout ->
			renderResult compiled,
		, 500
