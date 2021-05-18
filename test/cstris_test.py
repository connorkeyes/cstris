
from app.cstris import generate_code

def test_generate_code():
    assert generate_code("test",12.75,2)[0] == 't'
    assert generate_code("test",12.75,2)[25:29] == '12.75'
    assert generate_code("test",12.75,2)[54] == '2'