from flask import Response, jsonify
from xml.etree.ElementTree import Element, tostring, SubElement

def dict_to_xml(tag, data):
    """Converts a dictionary to XML."""
    element = Element(tag)
    for key, val in data.items():
        child = SubElement(element, key)
        child.text = str(val)
    return tostring(element)

def create_response(data, content_type):
    """Creates a response with the desired content type."""
    if content_type == 'application/xml':
        if isinstance(data, list):
            root = Element('items')
            for item in data:
                item_element = SubElement(root, 'item')
                for key, val in item.items():
                    child = SubElement(item_element, key)
                    child.text = str(val)
            xml_data = tostring(root)
        else:
            xml_data = dict_to_xml('response', data)
        return Response(xml_data, content_type='application/xml')
    else:  # Default to JSON
        return Response(jsonify(data).data, content_type='application/json')
