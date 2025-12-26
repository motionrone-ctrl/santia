import { Navbar } from '../components/Navbar';
import { Hero } from '../components/Hero';
import { Specialties } from '../components/Specialties';
import { HowItWorks } from '../components/HowItWorks';
import { TrustSection } from '../components/TrustSection';
import { FAQ } from '../components/FAQ';
import { Footer } from '../components/Footer';

export const Home = () => {
  return (
    <div className="min-h-screen" data-testid="home-page">
      <Navbar />
      <main>
        <Hero />
        <Specialties />
        <HowItWorks />
        <TrustSection />
        <FAQ />
      </main>
      <Footer />
    </div>
  );
};

export default Home;
