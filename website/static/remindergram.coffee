$ ->
	# Dom elements
	$form       = $ 'form.remindergram'
	$service    = $ '#service'
	$identifier = $ '#identifier'

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
		$.post $form.attr( 'action' ), data, ( data ) ->
			console.log data

	parseFormData = ( $form ) ->
		return _.reduce $form.serializeArray(), ( data, pair ) ->
			data[ pair.name ] = pair.value
			return data
		, {}

