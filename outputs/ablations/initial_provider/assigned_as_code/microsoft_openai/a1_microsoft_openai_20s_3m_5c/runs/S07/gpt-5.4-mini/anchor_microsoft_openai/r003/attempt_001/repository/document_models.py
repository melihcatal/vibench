def _bbox_from_polygon(polygon):
    if not polygon:
        return None
    xs = [point.x for point in polygon]
    ys = [point.y for point in polygon]
    return {'x0': min(xs), 'y0': min(ys), 'x1': max(xs), 'y1': max(ys)}


def normalize_lines(result):
    lines = []
    for page in getattr(result, 'pages', []) or []:
        for line in getattr(page, 'lines', []) or []:
            lines.append({'text': line.content, 'bbox': _bbox_from_polygon(getattr(line, 'polygon', None))})
    return lines


def normalize_tables(result):
    tables = []
    for table in getattr(result, 'tables', []) or []:
        cells = []
        for cell in getattr(table, 'cells', []) or []:
            cells.append({
                'row_index': cell.row_index,
                'column_index': cell.column_index,
                'content': cell.content,
                'kind': getattr(cell, 'kind', None),
            })
        tables.append({'row_count': table.row_count, 'column_count': table.column_count, 'cells': cells})
    return tables


def normalize_key_values(result):
    pairs = []
    for kv in getattr(result, 'key_value_pairs', []) or []:
        pairs.append({
            'key': getattr(getattr(kv, 'key', None), 'content', None),
            'value': getattr(getattr(kv, 'value', None), 'content', None),
        })
    return pairs


def normalize_layout(result):
    return {
        'pages': len(getattr(result, 'pages', []) or []),
        'lines': normalize_lines(result),
        'tables': normalize_tables(result),
    }
