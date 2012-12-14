$ ->
	# Dom elements
	$form       = $ 'form.remindergram'
	$identifier = $ '#identifier'
	$result     = $ '.result'

	# Service/identify map
	services =
		'Instagram' : 'Username'
		'WordPress' : 'Blog address'
		'Tumblr'    : 'Blog address'
		'RSS'       : 'Feed address'

	# AJAX requests
	activeRequest = false

	# Listen on service buttons
	$form.find( '.btn' ).on 'click', ( event ) ->
		event.preventDefault()
		$form.find( '.btn' ).removeClass 'active'
		$( this ).addClass 'active'
		doService $( event.target ).text()

	getActiveService = ->
		active = $form.find '.btn.active'
		if active
			active.text()
		else
			''

	doService = ( name )->
		setIdentifer services[name]

	setIdentifer = ( placeholder ) ->
		$('label[for="identifier"]').text "Enter #{placeholder}"
		$identifier.attr 'placeholder', placeholder

	# Listen on form submit
	$form.on 'submit', ( event ) ->
		event.preventDefault()

		@activeRequest.abort() if @activeRequest

		data = parseFormData $form
		timer = waitingPanda()
		@activeRequest = $.post $form.attr( 'action' ), data, ( response ) ->
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
		inputs = _.reduce $form.serializeArray(), ( data, pair ) ->
			data[ pair.name ] = pair.value
			return data
		, {}

		_.extend inputs, { 'service': getActiveService() }

	renderSucces = ( response ) ->
		compiled = _.template '
			<ul>
			<% _.each(photos, function(photo) { %>
				<li><img src="<%= photo %>"></li> <%
			}); %>
			</ul>',
			photos: response

		renderResult compiled

	renderError = ( response ) ->
		compiled = _.template 'Oops, there was an error: <%= error %>', response
		renderResult compiled

	renderResult = ( html ) ->
		$result.html html

	waitingPanda = ->
		compiled = _.template '<img src="<%= src %>">',
			src: 'http://25.media.tumblr.com/tumblr_ly2em98lub1r3m4cbo1_400.gif'

		setTimeout ->
			renderResult compiled,
		, 500
