from flask import Flask, render_template, session, redirect, request
from functools import wraps
from DataBase import login_user, getData


def login_required_for_id(f):

  @wraps(f)
  def decorated_function(id, *args, **kwargs):
    if 'username' not in session or session['username'] != id:
      return redirect('/login')
    return f(id, *args, **kwargs)

  return decorated_function


app = Flask(__name__)
app.secret_key = 'secretestkey'


@app.route('/')
def home():
  return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

  if request.method == 'POST':
    user = request.form['username']
    pw = request.form['password']
    data = login_user(user, pw)
    if data:
      session['username'] = data[0]
      return redirect('/dashboard/{}'.format(user))

    else:
      print('error')

  return render_template('login.html')


@app.route("/dashboard/<id>")
@login_required_for_id
def data_page(id):
  data = getData()
  int_sec = data['int_sec']
  int_top = data['int_top']
  int_pes = data["int_pes"]
  rel_sec = data['rel_sec']
  rel_top = data['rel_top']
  rel_pes = data['rel_pes']
  org_yr_freq= data['org_yr_freq']
  pol_yr_freq= data['pol_yr_freq']
  env_yr_freq= data['env_yr_freq']
  hlt_yr_freq= data['hlt_yr_freq']
  lif_yr_freq= data['lif_yr_freq']
  tech_yr_freq= data['tech_yr_freq']
  eco_yr_freq= data['eco_yr_freq']
  ind_yr_freq= data['ind_yr_freq']
  soc_yr_freq= data['soc_yr_freq']
  gov_cou_freq = data['gov_cou_freq']
  tra_cou_freq = data['tra_cou_freq']
  sec_cou_freq = data['sec_cou_freq']
  ene_cou_freq = data['ene_cou_freq']
  ret_cou_freq = data['ret_cou_freq']
  triple_data = data["triple_data"]

  return render_template('dashboard.html',
                         username=id,
                         int_sec=int_sec,
                         int_top=int_top,
                         int_pes=int_pes,
                         rel_sec=rel_sec,
                         rel_top=rel_top,
                         rel_pes=rel_pes,
                         Organization = org_yr_freq,
                        Political = pol_yr_freq,
                        Environmental = env_yr_freq,
                        Health = hlt_yr_freq,
                        Lifestyles = lif_yr_freq,
                         Technological = tech_yr_freq,
                        Economic = eco_yr_freq,
                        Industries = ind_yr_freq,
                        Social = soc_yr_freq,
                         gov_freq = gov_cou_freq,
                         tra_freq = tra_cou_freq,
                         sec_freq = sec_cou_freq,
                         ene_freq = ene_cou_freq,
                         ret_freq = ret_cou_freq,
                         triple_data = triple_data,
        
                        )


if __name__ == '__main__':
  app.run(host='0.0.0.0', port='8080')
