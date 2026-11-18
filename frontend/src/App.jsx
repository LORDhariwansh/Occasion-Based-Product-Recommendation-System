import { useState } from "react";
import { ArrowUpRight, Gift, Search, Sparkles } from "lucide-react";
import ProductCard from "./components/ProductCard";
import {
  EmptyState,
  ErrorState,
  LoadingState,
} from "./components/ResultStates";
import { getRecommendations } from "./services/api";

const suggestions = [
  "Birthday celebration",
  "Wedding present",
  "Diwali gifting",
  "Housewarming gift",
  "Corporate gifting",
  "Thank-you gift",
  "Graduation celebration",
  "Something under ₹1000",
];

export default function App() {
  const [occasion, setOccasion] = useState("");
  const [state, setState] = useState({ status: "idle", data: null, error: "" });
  const isLoading = state.status === "loading";

  async function search(event, value = occasion) {
    event?.preventDefault();
    const query = value.trim();
    if (!query) {
      setState({
        status: "error",
        data: null,
        error: "Enter an occasion, celebration, or budget to begin.",
      });
      return;
    }
    setOccasion(query);
    setState({ status: "loading", data: null, error: "" });
    try {
      const data = await getRecommendations(query);
      setState({ status: "success", data, error: "" });
    } catch (error) {
      setState({ status: "error", data: null, error: error.message });
    }
  }

  return (
    <main className="min-h-[100dvh] overflow-x-hidden bg-slate-50 text-slate-950">
      <header className="mx-auto flex max-w-7xl items-center justify-between px-5 py-5 sm:px-8 lg:py-6">
        <a
          href="#top"
          className="flex items-center gap-3 font-semibold tracking-tight text-slate-950"
        >
          <span className="grid size-10 place-items-center rounded-xl bg-[#155e75] text-white shadow-[0_8px_20px_rgba(21,94,117,0.18)]">
            <Gift size={20} strokeWidth={1.8} />
          </span>
          <span>EMILO Gift Finder</span>
        </a>
        <span className="hidden text-sm font-medium text-slate-500 sm:block">
          Thoughtful gifting, simply matched
        </span>
      </header>

      <section
        id="top"
        className="mx-auto grid max-w-7xl gap-10 px-5 pb-14 pt-8 sm:px-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-center lg:gap-16 lg:pb-20 lg:pt-16"
      >
        <div className="max-w-2xl">
          <p className="mb-5 inline-flex items-center gap-2 rounded-full border border-cyan-900/15 bg-cyan-50 px-3 py-1.5 text-sm font-semibold text-[#155e75]">
            <Sparkles size={15} strokeWidth={1.8} />
            Occasion-based recommendations
          </p>
          <h1 className="text-4xl font-semibold tracking-[-0.055em] text-slate-950 sm:text-6xl">
            Find the perfect gift for any occasion.
          </h1>
          <p className="mt-5 max-w-xl text-lg leading-8 text-slate-600">
            Discover thoughtful products for celebrations, festivals,
            milestones, and special moments.
          </p>
        </div>
        <aside className="rounded-3xl border border-slate-200 bg-white p-5 shadow-[0_24px_60px_rgba(15,23,42,0.08)] sm:p-7">
          <form onSubmit={search}>
            <label
              htmlFor="occasion"
              className="text-sm font-semibold text-slate-800"
            >
              What is the occasion?
            </label>
            <div className="mt-3 flex flex-col gap-3 sm:flex-row">
              <input
                id="occasion"
                value={occasion}
                onChange={(event) => setOccasion(event.target.value)}
                placeholder="e.g. Diwali celebration or thank-you gift"
                className="min-w-0 flex-1 rounded-xl border border-slate-300 bg-white px-4 py-3.5 text-slate-950 outline-none transition placeholder:text-slate-400 focus:border-[#155e75] focus:ring-4 focus:ring-cyan-100"
              />
              <button
                type="submit"
                disabled={isLoading}
                className="inline-flex min-h-12 shrink-0 items-center justify-center gap-2 rounded-xl bg-[#155e75] px-5 py-3 font-semibold text-white transition hover:bg-[#164e63] disabled:cursor-wait disabled:bg-slate-500 active:translate-y-px"
              >
                <Search size={18} />
                {isLoading ? "Finding gifts" : "Find gifts"}
              </button>
            </div>
          </form>
          <div className="mt-5 border-t border-slate-100 pt-5">
            <p className="mb-3 text-xs font-semibold uppercase tracking-[0.12em] text-slate-400">
              Try an occasion
            </p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => search(null, suggestion)}
                  disabled={isLoading}
                  className="rounded-full border border-slate-200 bg-slate-50 px-3 py-1.5 text-left text-xs font-medium text-slate-600 transition hover:border-cyan-800/30 hover:bg-cyan-50 hover:text-[#155e75] disabled:cursor-wait disabled:opacity-60"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        </aside>
      </section>

      <section
        aria-live="polite"
        className="mx-auto max-w-7xl px-5 pb-16 sm:px-8 lg:pb-20"
      >
        {state.status === "idle" && (
          <div className="rounded-3xl border border-cyan-900/10 bg-[#e7f3f5] px-6 py-8 sm:px-10 sm:py-9">
            <p className="text-sm font-semibold text-[#155e75]">
              Made for meaningful moments
            </p>
            <div className="mt-3 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
              <p className="max-w-2xl text-xl font-medium tracking-tight text-slate-900">
                Tell us the occasion and we will find relevant products from the
                available catalog.
              </p>
              <ArrowUpRight
                className="hidden shrink-0 text-[#155e75] sm:block"
                size={28}
              />
            </div>
          </div>
        )}
        {state.status === "loading" && <LoadingState />}
        {state.status === "error" && <ErrorState message={state.error} />}
        {state.status === "success" &&
          (state.data.recommendations.length ? (
            <>
              <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
                <div>
                  <p className="text-sm font-semibold text-[#155e75]">
                    Recommended for
                  </p>
                  <h2 className="mt-1 text-3xl font-semibold tracking-tight text-slate-950 sm:text-4xl">
                    {state.data.occasion}
                  </h2>
                </div>
                <p className="rounded-full border border-slate-200 bg-white px-3 py-1.5 text-sm font-medium text-slate-600">
                  {state.data.total_results} catalog match
                  {state.data.total_results === 1 ? "" : "es"}
                </p>
              </div>
              <div className="grid grid-cols-1 gap-5 md:grid-cols-2 xl:grid-cols-3">
                {state.data.recommendations.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>
            </>
          ) : (
            <EmptyState message={state.data.message} />
          ))}
      </section>
    </main>
  );
}
