'use client';
import React, { useState } from 'react';

type Analysis = {
  dominant_colors: { rgb: number[]; hex: string; proportion: number }[];
  brightness: number;
  saturation: number;
  palette_name: string;
  style_profile: {
    recommended_styles: string[];
    why: { palette_match: string; occasions: string[]; goals: string[] };
    fit_tips: string[];
    starter_capsule: string[];
  };
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Page() {
  const [file, setFile] = useState<File | null>(null);
  const [survey, setSurvey] = useState({
    gender: '',
    ageRange: '',
    primaryOccasions: [] as string[],
    styleGoals: [] as string[],
    comfortVsAesthetic: 'balanced',
    colorPrefs: [] as string[],
    budget: 'mid'
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<Analysis | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleOccasionToggle = (v: string) => {
    setSurvey(s => ({
      ...s,
      primaryOccasions: s.primaryOccasions.includes(v) 
        ? s.primaryOccasions.filter(x => x !== v) 
        : [...s.primaryOccasions, v]
    }));
  };

  const handleGoalToggle = (v: string) => {
    setSurvey(s => ({
      ...s,
      styleGoals: s.styleGoals.includes(v) 
        ? s.styleGoals.filter(x => x !== v) 
        : [...s.styleGoals, v]
    }));
  };

  const handleColorToggle = (v: string) => {
    setSurvey(s => ({
      ...s,
      colorPrefs: s.colorPrefs.includes(v) 
        ? s.colorPrefs.filter(x => x !== v) 
        : [...s.colorPrefs, v]
    }));
  };

  const submit = async () => {
    if (!file) { setError('Please upload an outfit photo first.'); return; }
    setError(null);
    setLoading(true);
    try {
      const fd = new FormData();
      fd.append('image', file);
      fd.append('survey_json', JSON.stringify(survey));
      const resp = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        body: fd
      });
      if (!resp.ok) throw new Error('API error');
      const data = await resp.json();
      setResult(data);
    } catch (e:any) {
      setError(e.message || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  const Chip = ({label, active, onClick}:{label:string, active:boolean, onClick:()=>void}) => (
    <button onClick={onClick} style={{padding:'6px 10px', margin:4, borderRadius:20, border: active? '2px solid black':'1px solid #ccc', background: active? '#f0f0f0':'#fff', cursor:'pointer'}}>{label}</button>
  );

  return (
    <main>
      <section style={{display:'grid', gap:16}}>
        <div style={{border:'1px solid #eee', padding:16, borderRadius:12}}>
          <h2>Upload an outfit photo</h2>
          <input type="file" accept="image/*" onChange={e=> setFile(e.target.files?.[0] || null)} />
        </div>

        <div style={{border:'1px solid #eee', padding:16, borderRadius:12}}>
          <h2>Quick Survey</h2>
          <div style={{display:'grid', gap:12}}>
            <label>
              Gender:
              <select value={survey.gender} onChange={e=> setSurvey({...survey, gender: e.target.value})}>
                <option value="">Prefer not to say</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="nonbinary">Non-binary</option>
              </select>
            </label>

            <label>
              Age range:
              <select value={survey.ageRange} onChange={e=> setSurvey({...survey, ageRange: e.target.value})}>
                <option value="">Select</option>
                <option value="teen">13–19</option>
                <option value="20s">20–29</option>
                <option value="30s">30–39</option>
                <option value="40s">40–49</option>
                <option value="50+">50+</option>
              </select>
            </label>

            <div>
              <div>Primary occasions:</div>
              {['Work','School','Dates','Nights Out','Weddings','Interviews','Travel'].map(o=> (
                <Chip key={o} label={o} active={survey.primaryOccasions.includes(o)} onClick={()=>handleOccasionToggle(o)} />
              ))}
            </div>

            <div>
              <div>Style goals:</div>
              {['Look taller','Look more muscular','More professional','Be more expressive','Low maintenance'].map(o=> (
                <Chip key={o} label={o} active={survey.styleGoals.includes(o)} onClick={()=>handleGoalToggle(o)} />
              ))}
            </div>

            <label>
              Comfort vs. Aesthetic:
              <select value={survey.comfortVsAesthetic} onChange={e=> setSurvey({...survey, comfortVsAesthetic: e.target.value})}>
                <option value="comfort">Comfort</option>
                <option value="balanced">Balanced</option>
                <option value="aesthetic">Aesthetic</option>
              </select>
            </label>

            <div>
              <div>Favorite colors:</div>
              {['Black','White','Grey','Navy','Olive','Tan','Cream','Red','Blue','Green','Yellow'].map(c=> (
                <Chip key={c} label={c} active={survey.colorPrefs.includes(c)} onClick={()=>handleColorToggle(c)} />
              ))}
            </div>

            <label>
              Budget:
              <select value={survey.budget} onChange={e=> setSurvey({...survey, budget: e.target.value})}>
                <option value="low">Low</option>
                <option value="mid">Mid</option>
                <option value="high">High</option>
              </select>
            </label>
          </div>
        </div>

        <div>
          <button onClick={submit} disabled={loading} style={{padding:'10px 14px', borderRadius:10, border:'1px solid #222', cursor:'pointer'}}>
            {loading ? 'Analyzing...' : 'Analyze Style'}
          </button>
        </div>

        {error && <div style={{color:'crimson'}}>{error}</div>}

        {result && (
          <div style={{border:'1px solid #eee', padding:16, borderRadius:12}}>
            <h2>Your Style Profile</h2>
            <p><strong>Palette:</strong> {result.palette_name} | <strong>Brightness:</strong> {result.brightness} | <strong>Saturation:</strong> {result.saturation}</p>
            <div style={{display:'flex', gap:8, flexWrap:'wrap', marginBottom:8}}>
              {result.dominant_colors.map((c, i)=> (
                <div key={i} title={`${c.hex} (${Math.round(c.proportion*100)}%)`} style={{width:48, height:48, borderRadius:8, border:'1px solid #ccc', background:c.hex}}/>
              ))}
            </div>

            <h3>Recommended Styles</h3>
            <ul>
              {result.style_profile.recommended_styles.map((s,i)=>(<li key={i}>{s}</li>))}
            </ul>

            <h3>Fit Tips</h3>
            <ul>
              {result.style_profile.fit_tips.map((s,i)=>(<li key={i}>{s}</li>))}
            </ul>

            <h3>Starter Capsule</h3>
            <ul>
              {result.style_profile.starter_capsule.map((s,i)=>(<li key={i}>{s}</li>))}
            </ul>

            <details>
              <summary>Why these picks?</summary>
              <pre style={{whiteSpace:'pre-wrap'}}>{JSON.stringify(result.style_profile.why, null, 2)}</pre>
            </details>
          </div>
        )}
      </section>
    </main>
  );
}
