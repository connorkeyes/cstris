# Keep getting ModuleNotFoundError: No module named 'app'
# Cannot for the life of me figure out what I am doing wrong; pytest aborted

from app.cstris import generate_code
from app.cstris import accept_challenge

def test_generate_code():
    assert generate_code("test",12.75,2)[0] == 't'
    assert generate_code("test",12.75,2)[25:29] == '12.75'
    assert generate_code("test",12.75,2)[54] == '2'

def test_accept_challenge():
    assert accept_challenge("CTrain963982653189383087304106411.0369488367480975665396228721") == [1, "CTrain", 11.03]

